import Resize_functions
import Distribution
import json

with open('Fine-Grained-Image-Classification/Image_preparation/Config.json') as f:
    config = json.load(f)

dataset_dir = config['dataset_dir']
output_dir = config['output_dir']

# This one is to resize the images in the dataset based on the AVERAGE size of the images in the dataset.
avg_height, avg_width = Resize_functions.mean_images_sizes(dataset_dir)

# Resizing the images in the dataset based on the AVERAGE size of the images in the dataset.
Resize_functions.resize_with_padding(dataset_dir, output_dir, int(avg_width), int(avg_height))

'''
# This one is to resize the images in the dataset based on the MODE size of the images in the dataset.
mode_height, mode_width = Resize_functions.mode_images_mode_sizes(dataset_dir)

# Resizing the images in the dataset based on the MODE size of the images in the dataset.
Resize_functions.resize_with_padding(dataset_dir, output_dir, mode_width, mode_height)
'''

Dist = Distribution.plot_image_size_distribution(dataset_dir)