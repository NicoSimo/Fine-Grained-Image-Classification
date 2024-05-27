import Resize_functions
import json

with open('Image_preparation/Config.json') as f:
    config = json.load(f)

dataset_dir = config['dataset_dir']
output_dir = config['output_dir']

print(dataset_dir, '\n', output_dir)

avg_height, avg_width = Resize_functions.images_sizes(dataset_dir)

Resize_functions.resize_with_padding(dataset_dir, output_dir, int(avg_width), int(avg_height))
