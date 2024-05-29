import torch.nn as nn
import torch.optim as optim
import torch.utils
import torch.utils.data
from torchvision.io import read_image
from PIL import Image
from torch.utils.data import Dataset,DataLoader
from torchvision import transforms
import torch

import os
import skimage.io as io
import pandas as pd
import json 

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

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the outer directory where Config.json file is located
MLCOMP_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Path to the config file
# Config.json file contains the paths to the input dataset and output dataset directories
config_path = os.path.join(MLCOMP_dir, 'Config.json')

with open(config_path) as f:
    config = json.load(f)

# Get the /flowers-102 absolute path
Flower102_dir = os.path.abspath(os.path.join(config['output_dir_flowers102'], os.pardir))

# Get the statistics.json file path where the std and mean are stored
statistics_path = os.path.join(Flower102_dir, 'statistics.json')

# Open the stats.json file and set the dictionary dataset_stats for normalization
with open(statistics_path) as f:
    dataset_stats = json.load(f)

# Directory containing the images
img_dir = config['output_dir_flowers102']

# Paths to the labels file
labels_file = config['output_labels_flowers102']

# Paths to the setid file
setid_file = config['output_setid_flowers102']

# Define any transformations (e.g., resizing, normalization)
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean = dataset_stats["mean"] , std = dataset_stats["std"]),
])

dataset = Flowers102Dataset(csv_file = labels_file, root_dir= img_dir, transform = transform)
train_set, test_set = torch.utils.data.random_split(dataset, [7000,1189])

train_loader = DataLoader(dataset=train_set, batch_size=32, shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size=32, shuffle=True)

image, label = dataset.__getitem__(100)
print(image, label)