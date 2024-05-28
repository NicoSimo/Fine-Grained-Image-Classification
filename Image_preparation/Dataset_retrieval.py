import Resize_functions
import Distribution
import json
import os

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the outer directory where Config.json file is located
MLCOMP_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

# Path to the config file
# Config.json file contains the paths to the input dataset and output dataset directories
config_path = os.path.join(MLCOMP_dir, 'config.json')

with open(config_path) as f:
    config = json.load(f)

dataset_dir = config['dataset_dir_flowers102']
output_dir = config['output_dir_flowers102']

# FGVC Aircraft dataset needs at least RATIO = 0.98 in the resize_with_padding function to crop out the desctiption text from the images
#dataset_dir = config['dataset_dir_fgvc-aircraft']
#output_dir = config['output_dir_fgvc-aircraft']

'''
# This one is to resize the images in the dataset based on the AVERAGE size of the images in the dataset.
avg_height, avg_width = Resize_functions.mean_images_sizes(dataset_dir)

# Resizing the images in the dataset based on the AVERAGE size of the images in the dataset.
Resize_functions.resize_with_padding(dataset_dir, output_dir, int(avg_width), int(avg_height))

'''

# This one is to resize the images in the dataset based on the MODE size of the images in the dataset.
mode_height, mode_width = Resize_functions.mode_images_mode_sizes(dataset_dir)

# Resizing the images in the dataset based on the MODE size of the images in the dataset.
Resize_functions.resize_with_padding(dataset_dir, output_dir, mode_width, mode_height)


#Dist = Distribution.plot_image_size_distribution(dataset_dir)