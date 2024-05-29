import Resize_functions
import Distribution
import json
import os
import Mat_to_csv

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the outer directory where Config.json file is located
MLCOMP_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

# Path to the config file
# Config.json file contains the paths to the input dataset and output dataset directories
config_path = os.path.join(MLCOMP_dir, 'config.json')

with open(config_path) as f:
    config = json.load(f)

################################################ Flowers dataset ################################################

output_dir = config['output_dir_flowers102']

statistics_file = config['statistics_flowers102']

Resize_functions.compute_mean_std(output_dir, statistics_file)
