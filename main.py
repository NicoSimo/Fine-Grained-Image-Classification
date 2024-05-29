import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import skimage.io as io
import pandas as pd
from Dataset_classes.Flowers.Flowers_Dataset import Flowers102Dataset as Flowers_Dataset

import os
import json
import numpy as np

import matplotlib.pyplot as plt


################################################# Files import  #################################################

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
 

################################################# Dataset preparation  #################################################
dataset = Flowers_Dataset(csv_file = labels_file, root_dir= img_dir)
train_set, test_set = torch.utils.data.random_split(dataset, [7000,1189])

train_loader = DataLoader(dataset=train_set, batch_size=32, shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size=32, shuffle=True)

# Testing getitem and viewitem with a random index
IDX = 800
image, label = dataset.__getitem__(IDX)
#print(image, label)
#dataset.__viewitem__(index = IDX, mean = dataset_stats["mean"], std = dataset_stats["std"])


################################################# DataLoader preparation  #################################################

def get_data(batch_size, test_batch_size = 256, num_workers = 4, mean = None, std=None):

    if mean is None or std is None:
        transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean = dataset_stats["mean"] , std = dataset_stats["std"]),
        ])
        # Dataset loader 
        full_training_data = Flowers_Dataset(csv_file = labels_file, root_dir= img_dir, transform = transform)
        
        images = torch.stack([image for image, _ in full_training_data], dim=3)
        mean = torch.mean(images)
        std = torch.std(images)
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean = mean , std = std),
    ])

    # Dataset loader
    full_training_data = Flowers_Dataset(csv_file = labels_file, root_dir= img_dir, transform = transform)
    
    # Dataset split
    num_samples = full_training_data.__len__()
    train_size = int(0.6*num_samples)
    val_size = int(0.2*num_samples)
    test_size = num_samples - train_size - val_size
    train_set, val_set, test_set = torch.utils.data.random_split(full_training_data, [train_size, val_size, test_size])

    train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(dataset=val_set, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    test_loader = DataLoader(dataset=test_set, batch_size=test_batch_size, shuffle=True, num_workers=num_workers)

    return train_loader, val_loader, test_loader

train_loader, val_loader, test_loader = get_data(128)
i = iter(train_loader)
a = next(i)
for t in a: 
    print(t.dtype)