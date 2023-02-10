import torch
from calcimetry.ml.train import training
from calcimetry.ml.config import Config
from clearml import Task


from ignite.contrib.handlers.clearml_logger import ClearMLLogger


if __name__ == '__main__':
    import os
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

    # set up device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    config = {
        'seed': 1,
         # dataset
        'host': 'localhost',
        'port': 27017,
        'batch_size': 14,
        'train_val_ratio': .8,

         # learning
        'optimizer': 'sgd',
        'lr': 1e-6,
        'momentum': 0.9,
        "weight_decay": 1e-4,
        "dropout": 0.9,

         # lr_scheduler
        "with_scheduler": False,
        "num_warmup_epochs": 1,
        

        'num_epochs': 6,
        #'modelname': "resnet18",
        #'modelname': "densenet169",
        'modelname': "alexnet",
        'save_best': False
    }


    task = Task.init(
        project_name=Config.PROJECT,
        task_name=Config.TASK
    )
    task.connect(config)

    # To utilize other loggers we need to change the object here
    clearml_logger = ClearMLLogger(
        project_name=Config.PROJECT, 
        task_name=Config.TASK
        ) 

    
    try:
        training(config=config, device=device, logger=clearml_logger)
    except Exception as er:
        print(er)

    print(task.get_last_scalar_metrics())