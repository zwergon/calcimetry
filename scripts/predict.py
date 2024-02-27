import logging
import argparse

from torch.utils.data import DataLoader

from iapytoo.utils.config import Config

from ai.training import CalciTraining
from ai.dataset import CalciDataset
import matplotlib.pyplot as plt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("dataset", help="path to parquet file")
    parser.add_argument("run_id", help="path to checkpoint")
    parser.add_argument(
        "-tu",
        "--tracking_uri",
        help="where to find run_id",
        type=str,
        default=None,
    )

    # INPUT Parameters
    args = parser.parse_args()
    config = Config.create_from_run_id(args.run_id, args.tracking_uri)
    config.dataset = args.dataset
    config.cuda = False

    logging.info(config)

    training = CalciTraining(config)

    train_dataset = CalciDataset(
        config, download=True, train=True, scaling=training.y_scaling
    )
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
    )

    test_dataset = CalciDataset(
        config, download=True, train=False, scaling=training.y_scaling
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
    )

    training.predict(loader=train_loader, run_id=args.run_id)
    train_pred = training.predictions

    training.predict(loader=test_loader)
    test_pred = training.predictions

    fig, axs = plt.subplots(nrows=1, ncols=1)
    fig.suptitle("Calcimetry actual versus predicted")
    axs.scatter(train_pred.actual, train_pred.predicted)
    axs.scatter(test_pred.actual, test_pred.predicted)
    axs.set_xlabel("actual")
    axs.set_ylabel("predicted")
    plt.show()
