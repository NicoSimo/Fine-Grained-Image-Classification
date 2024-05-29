# Fine-Grained-Image-Classification

Repository for the Competition hosted at the end of the course "Introduction to Machine Learning" A.Y. 2023/2024 from the Master of Science in Data Science of the University of Trento.

The repository will be filled with different models in order to obtain the one with the highest performance (Accuracy).

To run the code you need the dataset (I downloaded it from pytorch) and a Config.json file I used to store the absolute paths of different files or directories. 

Example 'Config.json' :

{
    "dataset_dir_flowers102": "/Users/USERNAME/Desktop/PARENT_DIRECTORY/PARENT_DIRECTORY/PARENT_DIRECTORY/Original_datasets/flowers-102/jpg",
    "dataset_labels_flowers102": "/Users/USERNAME/Desktop/PARENT_DIRECTORY/PARENT_DIRECTORY/PARENT_DIRECTORY/Original_datasets/flowers-102/imagelabels.mat",

    "output_dir_flowers102": "/Users/USERNAME/Desktop/PARENT_DIRECTORY/PARENT_DIRECTORY/PARENT_DIRECTORY/Resized_datasets/flowers-102/jpg",
    "output_labels_flowers102": "/Users/USERNAME/Desktop/PARENT_DIRECTORY/PARENT_DIRECTORY/PARENT_DIRECTORY/Resized_datasets/flowers-102/imagelabels.csv",

    "statistics_flowers102" : "/Users/USERNAME/Desktop/PARENT_DIRECTORY/PARENT_DIRECTORY/PARENT_DIRECTORY/Resized_datasets/flowers-102/statistics.json",
}

<USAGE> :
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the outer directory where Config.json file is located
MLCOMP_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Path to the config file
# Config.json file contains the paths to the input dataset and output dataset directories
config_path = os.path.join(MLCOMP_dir, 'Config.json')

with open(config_path) as f:
    config = json.load(f)

img_dir = config['output_dir_flowers102']
