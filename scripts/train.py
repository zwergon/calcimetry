from torch.utils.data import DataLoader

from iapytoo.utils.config import Config
from iapytoo.utils.arguments import parse_args
from ai.dataset import CalciDataset
from ai.training import CalciTraining

if __name__ == "__main__":
    args = parse_args()

    # INPUT Parameters
    config = Config.create_from_args(args)

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

    training.fit(train_loader=train_loader, valid_loader=test_loader)
