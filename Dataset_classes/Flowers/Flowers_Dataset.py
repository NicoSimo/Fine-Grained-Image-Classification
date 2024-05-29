import torch.utils
from torch.utils.data import Dataset
import torch

import os
import skimage.io as io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Flowers102Dataset(Dataset):
    def __init__ (self, csv_file, root_dir, transform = None):
        self.annotations = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        
    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        # Get the image name from the csv file and converts it in the format of the images in the folder. Example : 'image_00001.jpg'
        filename = 'image_' + str(self.annotations.iloc[index, 0]+1).zfill(5)
        img_path = os.path.join(self.root_dir, filename + '.jpg')

        image = io.imread(img_path)
        y_label = torch.tensor(int(self.annotations.iloc[index,1]))

        if self.transform:
            image = self.transform(image)
        
        return (image,y_label)

    def __viewitem__(self, index, mean, std) -> None:
        
        if self.transform:
            image = self.transform(image)
            
            mean = torch.tensor(mean).view(3, 1, 1)
            std = torch.tensor(std).view(3, 1, 1)

            image, label = Flowers102Dataset.__getitem__(self, index)
            unnormalized_image = image * std + mean

            # Convert the tensor to a NumPy array
            numpy_image = unnormalized_image.numpy()

            # Transpose the image to (H, W, C) format for matplotlib
            numpy_image = np.transpose(numpy_image, (1, 2, 0))

            # Clip values to [0, 1] range for display
            numpy_image = np.clip(numpy_image, 0, 1)

            # Plot the image using matplotlib
            plt.imshow(numpy_image)
        
        else :
            image, label = Flowers102Dataset.__getitem__(self, index)
            plt.imshow(image)
        plt.title(f"Label: {label.item()}")
        plt.show()