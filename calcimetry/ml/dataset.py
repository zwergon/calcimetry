import torch
from torch.utils.data import Dataset
from torchvision import transforms





class CalciDataset(Dataset):

    """
    According to https://pytorch.org/hub/pytorch_vision_alexnet/
    All pre-trained models (resnet, densenet, alexnet) expect input images normalized in the same way, 
    i.e. mini-batches of 3-channel RGB images of shape (3 x H x W), 
    where H and W are expected to be at least 224. 
    The images have to be loaded in to a range of [0, 1] 
    and then normalized using mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225].

    """

    @staticmethod
    def _default_transform():
        return  transforms.Compose([
                transforms.ConvertImageDtype(torch.float),
                transforms.Resize(224),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
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