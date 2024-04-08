from iapytoo.train.training import Training
from iapytoo.utils.config import Config
from iapytoo.train.models import ModelFactory
from iapytoo.predictions.plotters import ScatterPlotter
from iapytoo.metrics.creators import R2Creator
from iapytoo.dataset.scaling import Scaling

from ai.models import CalciResnet, VGG


class CalciTraining(Training):
    _metric_creators = [R2Creator()]

    stats = {"Calcimetry": {"mean": 0, "std": 1, "min": 0, "max": 100}}

    def __init__(self, config: Config) -> None:
        super().__init__(
            config,
            metric_creators=CalciTraining._metric_creators,
            prediction_plotter=ScatterPlotter(),
            y_scaling=Scaling.create("min_max", CalciTraining.stats, ["Calcimetry"]),
        )
        factory = ModelFactory()
        factory.register_model("resnet18", CalciResnet)
        factory.register_model("vgg", VGG)
