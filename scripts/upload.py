
from clearml import Dataset

def push_data():
    task = Dataset.create(dataset_name="Andras", dataset_project="models")
    task.add_files(path=f"./data/models")
    task.upload(show_progress=True)
    task.finalize()


if __name__ == '__main__':
    push_data()