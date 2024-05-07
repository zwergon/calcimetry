import os
from typing import Dict
import logging
import ray
from ray import tune
from torch.utils.data import DataLoader

from iapytoo.utils.config import Config
from ai.dataset import CalciDataset
from ai.training import CalciTraining


def calci_trainable(params: Dict):
    config = Config(params["json"])
    config.weight_decay = params["weight_decay"]
    config.type = params["type"]
    config.learning_rate = params["learning_rate"]
    config.batch_size = params["batch_size"]

    training = CalciTraining(config)
    train_dataset = CalciDataset(
        config, download=False, train=True, scaling=training.y_scaling
    )
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
    )

    test_dataset = CalciDataset(
        config, download=False, train=False, scaling=training.y_scaling
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
    )

    return training.fit(train_loader, test_loader)


if __name__ == "__main__":
    params = {
        "json": "/work/lecomtje/Repositories/calcimetry/git-calcimetry/scripts/tune.json",
        "learning_rate": tune.loguniform(3e-5, 4e-3),
        "weight_decay": tune.loguniform(3e-7, 1e-5),
        "batch_size": tune.choice([8, 64, 128]),
        "type": tune.choice(["resnet12", "resnet18", "vgg"]),
    }

    # os.environ["RAY_USE_XRAY"] = "1"
    ray.init(address="auto")

    tuner = tune.Tuner(
        trainable=tune.with_resources(calci_trainable, resources={"gpu": 0.5}),
        tune_config=tune.TuneConfig(
            num_samples=100,
            metric="loss",
            mode="min",
        ),
        param_space=params,
    )

    result = tuner.fit()

    logging.info(f"Best config: {result.get_best_result(metric='loss', mode='min')}")

    # logging.info(f"Best config: {result.get_best_result(metric='loss', mode='min')}")
