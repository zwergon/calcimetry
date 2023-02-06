import torch
from calcimetry.ml.train import training
from clearml import Task


def init(config):
    if config['with_clearml']:
        task = Task.init(
            project_name="Andras",
            task_name="training"
        )
        task.connect(config)


def close(config):
    if config['with_clearml']:
        Task.close()

if __name__ == '__main__':
    import os
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

    # set up device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    config = {
        'seed': 234,
         # dataset
        'host': 'localhost',
        'port': 27010,
        'batch_size': 4,
        'train_val_ratio': .8,

         # learning
        'lr': 1e-6,
        'momentum': 0.9,
        "weight_decay": 1e-4,
        "dropout": 0.9,

         # lr_scheduler
        "with_scheduler": False,
        "num_warmup_epochs": 1,
        

        'num_epochs': 3,
        'modelname': "resnet18",

        'with_clearml': True
    }

    init(config)
    
    try:
        training(config=config, device=device)
    except Exception as er:
        print(er)
        close(config)
      