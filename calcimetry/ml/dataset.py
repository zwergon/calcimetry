import torch
from torch.utils.data import Dataset
from torchvision import transforms





class CalciDataset(Dataset):

    @staticmethod
    def _default_transform():
        return  transforms.Compose([
                transforms.ConvertImageDtype(torch.float),
                transforms.Resize(224)
            ])


    def __init__(self, tuples: list):
        size = len(tuples)
        first_img = tuples[0][0]
        self.images = torch.empty(size, first_img.shape[2], first_img.shape[1], first_img.shape[0], dtype=torch.uint8)
        self.calcimetries = torch.empty(size, 1, dtype=torch.float32)

        self.transform = self._default_transform()

        for idx, t in enumerate(tuples):
            self.images[idx, : , :, :] = torch.from_numpy(t[0].copy()).permute(2, 1, 0)
            self.calcimetries[idx, 0] = float(t[1])
      

    def __getitem__(self, index):
        img = self.images[index, : , : , :]
        calci = self.calcimetries[index]
        return self.transform(img), calci
        

    def __len__(self):
        return self.calcimetries.shape[0]


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from calcimetry.ml import generate_datasets
  
  
    train_dataset, test_dataset = generate_datasets(port=27017)

    img, val = train_dataset[0]
    print(val)
    print(len(train_dataset))
    plt.imshow(img[0, : , :])
    plt.show()