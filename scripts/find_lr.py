from torch.utils.data import DataLoader

from iapytoo.utils.config import Config
from iapytoo.utils.arguments import parse_args
from ai.dataset import CalciDataset
from ai.training import CalciTraining

if __name__ == "__main__":
    args = parse_args()

    # INPUT Parameters
    config = Config.create_from_args(args)

    CalciTraining.init(config)

    train_dataset = CalciDataset(config, download=True, train=True)
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.num_workers,
    )

    training = CalciTraining(config)
    training.find_lr(train_loader=train_loader)
