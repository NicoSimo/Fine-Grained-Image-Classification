import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import skimage.io as io
import pandas as pd
from Dataset_classes.Flowers_Dataset import Flowers102Dataset as Flowers_Dataset

import os
import json

import matplotlib.pyplot as plt

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the outer directory where Config.json file is located
MLCOMP_dir = os.path.abspath(os.path.join(current_dir, os.pardir)) # os.pardir allows to go one directory back

# Path to the config file
# Config.json file contains the paths to the input dataset and output dataset directories
config_path = os.path.join(MLCOMP_dir, 'Config.json')

with open(config_path) as f:
    config = json.load(f)

# Get the statistics.json file path where the std and mean are stored
statistics_path = config['statistics_flowers102']

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

dataset = Flowers_Dataset(csv_file = labels_file, root_dir= img_dir, transform = transform)
train_set, test_set = torch.utils.data.random_split(dataset, [7000,1189])

train_loader = DataLoader(dataset=train_set, batch_size=32, shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size=32, shuffle=True)

image, label = dataset.__getitem__(100)

print(image, label)