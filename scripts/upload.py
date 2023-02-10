
from clearml import Dataset
from calcimetry.ml.config import Config

def push_data():
    task = Dataset.create(dataset_project=Config.PROJECT, dataset_name=Config.MODELS)
    task.add_files(path=f"./data/models")
    task.upload(show_progress=True)
    task.finalize()


if __name__ == '__main__':
    push_data()