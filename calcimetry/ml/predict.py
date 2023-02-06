
import torch
from ignite.engine import Engine
import ignite.distributed as idist
import numpy as np

class PredictEngine(Engine):

    def __init__(self, model):
        Engine.__init__(self, PredictEngine._predict)
        self.model = model
        self.initialize()

    def initialize(self):
        self.original = torch.tensor([]).to(idist.device())
        self.predicted = torch.tensor([]).to(idist.device())

    @staticmethod
    def _predict(engine, batch):
        engine.model.eval()
        with torch.no_grad():
            x, y = batch[0], batch[1]
            x = x.to(idist.device())
            y = y.to(idist.device())

            y_pred = engine.model(x)

            engine.predicted = torch.cat((engine.predicted, y_pred), 0)
            engine.original = torch.cat((engine.original, y), 0)

            return engine.predicted, engine.original

