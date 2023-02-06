import matplotlib.pyplot as plt
import numpy as np

from torch import nn, optim
from torch.utils.data import DataLoader
from ignite.engine import Events, create_supervised_trainer, create_supervised_evaluator
from ignite.metrics import Loss,  MeanAbsoluteError
from ignite.contrib.metrics.regression import R2Score, CanberraMetric
from ignite.handlers import Checkpoint, PiecewiseLinear
from ignite.utils import manual_seed, setup_logger
from ignite.contrib.handlers.clearml_logger import (
    ClearMLLogger,
    ClearMLSaver,
    global_step_from_engine,
)

from calcimetry.ml import generate_datasets
from calcimetry.ml.models import get_model
from calcimetry.ml.predict import PredictEngine




def get_dataflow(config, logger):

    train_dataset, val_dataset = generate_datasets(
        host=config['host'],
        port=config['port'],
        train_val_ratio=config['train_val_ratio']
    )

    n_elt_train = len(train_dataset)
    img, calci = train_dataset[n_elt_train // 2]
    print(img.shape)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.imshow(img[0, :, :])
    logger.report_matplotlib_figure(
        title="Train DataSet",
        series=str(calci),
        figure=fig
    )
    plt.close(fig)

    train_loader = DataLoader(
        train_dataset,
        batch_size=config['batch_size'],
        num_workers=1
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=config['batch_size'],
        num_workers=1
    )

    config["num_iters_per_epoch"] = len(train_loader)
    logger.report_text(f".. # of train samples {len(train_dataset)}")
    logger.report_text(f".. # of validation samples {len(val_dataset)}")
    logger.report_text(f".. # iters per epoch {config['num_iters_per_epoch']}")

    return train_loader, val_loader


def get_optimizer(config, model):

    if config['optimizer'] == 'sgd':
        optimizer = optim.SGD(
            model.parameters(),
            lr=config["lr"],
            momentum=config["momentum"]
            #weight_decay=config["weight_decay"],
            #nesterov=True,
        )
    elif config['optimizer'] == 'adam':
        optimizer = optim.Adam(
            model.parameters(),
            lr=config['lr']
        )
    else:
        raise Exception(f"unknown optimizer {config['optimizer']}")

    return optimizer


def get_criterion(device):
    return nn.MSELoss().to(device)


def get_lr_scheduler(config, optimizer):
    milestones_values = [
        (0, 0.0),
        (
            config["num_iters_per_epoch"] * config["num_warmup_epochs"],
            config["lr"],
        ),
        (config["num_iters_per_epoch"] * config["num_epochs"], 0.0),
    ]
    lr_scheduler = PiecewiseLinear(
        optimizer, param_name="lr", milestones_values=milestones_values
    )
    return lr_scheduler


def predict(engine, evaluator: PredictEngine, loader, logger, metrics):
    evaluator.initialize()
    evaluator.run(loader)
    y_pred, y = evaluator.state.output

    logger.report_text(f".. Prediction: {engine.state.epoch}")
    for k, v in metrics.items():
        val = max(0., evaluator.state.metrics[k])
        logger.report_scalar( k, "Predicted", iteration=engine.state.epoch, value=val)

    predicted = y_pred.cpu().numpy()
    original = y.cpu().numpy()

    scatter2d = np.hstack( (predicted, original) )

    logger.report_scatter2d(
        series='scatter',
        title=f"predicted/truth",
        iteration=engine.state.epoch,
        xaxis="predicted",
        yaxis=f"truth",
        scatter=scatter2d,
        mode='markers'
    )


def create_trainer(config, model, optimizer, criterion, lr_scheduler, logger, device):
    trainer = create_supervised_trainer(
        model,
        optimizer,
        criterion,
        device=device
    )
    
    if config['with_scheduler']:
        trainer.add_event_handler(Events.ITERATION_STARTED, lr_scheduler)

    return trainer


def run_validation(engine, evaluator, loader, tag, logger):
    
    state = evaluator.run(loader)
    logger.report_text(f".. {tag} - {engine.state.iteration} - mse: {state.metrics['mse']}")
    for m in ['mse',  "l1"]:
        logger.report_scalar(tag, m, iteration=engine.state.iteration, value=state.metrics[m])


def training(config, logger, device):

    manual_seed(config['seed'])

    train_loader, val_loader = get_dataflow(config, logger.clearml_logger)

    model = get_model(config, device=device)

    optimizer = get_optimizer(config, model)

    criterion = get_criterion(device)

    if config['with_scheduler']:
        lr_scheduler = get_lr_scheduler(config, optimizer)
    else:
        lr_scheduler = None

    trainer = create_trainer(
        config,
        model,
        optimizer,
        criterion,
        lr_scheduler,
        logger.clearml_logger,
        device
    )

    metrics = {
        'mse': Loss(criterion),
        'l1': MeanAbsoluteError()
    }

    train_evaluator = create_supervised_evaluator(model, metrics=metrics, device=device)
    val_evaluator = create_supervised_evaluator(model, metrics=metrics, device=device)
   
    for tag, evaluator, loader in [
        ("Training Metrics", train_evaluator, train_loader),
        ("Validation Metrics", val_evaluator, val_loader)
    ]:
        trainer.add_event_handler(
            Events.EPOCH_COMPLETED,
            run_validation,
            evaluator,
            loader,
            tag,
            logger.clearml_logger
        )

    test_metrics = {
        'r2': R2Score(),
        'canberra': CanberraMetric(),
        # 'manhattan': ManhattanDistance(),
        # 'max_absolute': MaximumAbsoluteError()
    }

    test_evaluator = PredictEngine(model)
    for k, v in test_metrics.items():
        v.attach(test_evaluator, k)
    
    trainer.add_event_handler(
        Events.EPOCH_COMPLETED(every=3),
        predict,
        test_evaluator,
        val_loader,
        logger.clearml_logger,
        test_metrics
    )

    if config['save_best']:
        to_save = {
            "trainer": trainer,
            "model": model
        }

        best_model_handler = Checkpoint(
            to_save,
            ClearMLSaver(logger, output_uri="s3://minio.10.68.0.250.nip.io:80/clearml"),
            filename_prefix="best",
            n_saved=2,
            global_step_transform=global_step_from_engine(trainer)
        )
        val_evaluator.add_event_handler(
            Events.COMPLETED,
            best_model_handler,
        )

    trainer.run(train_loader, max_epochs=config['num_epochs'])
