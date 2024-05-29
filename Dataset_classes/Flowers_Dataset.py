import torch.utils
from torch.utils.data import Dataset
import torch

import os
import skimage.io as io
import pandas as pd

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