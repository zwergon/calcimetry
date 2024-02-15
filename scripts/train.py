
from torch.utils.data import DataLoader

from iapytoo.train.models import ModelFactory
from iapytoo.utils.config import Config
from iapytoo.utils.arguments import parse_args
from iapytoo.train.training import Training
from iapytoo.train.metrics_collection import MetricCreator
from ai.dataset import CalciDataset
from ai.models import CalciResnet

from torchmetrics import R2Score

class R2Creator(MetricCreator):

    def __init__(self):
        super().__init__("r2")
        
    def create(self):
        return R2Score()

if __name__ == "__main__":

    factory = ModelFactory()
    factory.register_model("resnet18", CalciResnet)

    args = parse_args()

    # INPUT Parameters
    config = Config.create_from_args(args)
    config.type = 'resnet18'

    metric_creators = [R2Creator()]

    Training.seed(config)
    
    train_dataset = CalciDataset(
       config, 
       download=True, 
       version="1.0", 
       train=True
    )
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.num_workers,
    )

    test_dataset = CalciDataset(
        config, 
        download=True, 
        version="1.0", 
        train=False
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=config.num_workers,
    )

    training = Training(
        config,
        metric_creators = metric_creators)
    training.fit(train_loader=train_loader, valid_loader=test_loader)


    