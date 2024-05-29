import os
from PIL import Image
from collections import Counter
import numpy as np
import json

def resize_with_padding(dataset_dir: str, output_dir: str, target_width, target_height, CROP_RATIO = 1) -> None:
    '''
    Function to resize all images in the dataset_dir while preserving aspect ratio and adding padding to fit the target dimensions.
    
    dataset_dir = Input the directory where the images are stored
    output_dir = Input the directory where the cropped images will be stored
    target width = Input the target width of the image
    target height = Input the target height of the image
    CROP_RATIO = Input the ratio of the image to be cropped out from the bottom
    '''
    os.makedirs(output_dir, exist_ok=True)
    for root, _, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):

                img_path = os.path.join(root, file)
                img = Image.open(img_path)

                # Assuming copyright banner is at the bottom, you can crop it out
                original_width, original_height = img.size

                # Calculate scaling factor for resizing
                scale_factor_width = target_width / original_width
                scale_factor_height = target_height / original_height
                scale_factor = min(scale_factor_width, scale_factor_height)

                # Resize the image while preserving aspect ratio
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                # Calculate the cropping box to remove the copyright banner
                crop_box = (0, 0, new_width, int(new_height * CROP_RATIO))  # NECESSARY TO CROP OUT THE BANNER

                # Crop the image to remove the copyright banner
                cropped_img = resized_img.crop(crop_box)

                # Create a new blank image with the target dimensions
                padded_img = Image.new("RGB", (target_width, target_height), color="black")

                # Calculate the position to paste the cropped image to center it with padding
                paste_x = (target_width - new_width) // 2
                paste_y = (target_height - cropped_img.size[1]) // 2

                # Paste the cropped image onto the blank image with padding
                padded_img.paste(cropped_img, (paste_x, paste_y))

                output_path = os.path.join(output_dir, file)

                padded_img.save(output_path)

def mean_images_size(dataset_dir: str) -> None:
    '''
    Function that takes the dataset directory as input and calculates the average height and width.
    '''
    total_height = 0
    total_width = 0
    num_images = 0

    pixel_sum = np.zeros(3)
    pixel_squared_sum = np.zeros(3)
    total_pixels = 0

    for root, _, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path).convert('RGB')
                    width, height = img.size
                    np_img = np.array(img) / 255.0  # Normalize pixel values to [0, 1]

                    total_height += height
                    total_width += width
                    num_images += 1

                    pixel_sum += np_img.sum(axis=(0, 1))
                    pixel_squared_sum += (np_img ** 2).sum(axis=(0, 1))
                    total_pixels += height * width
                except Exception as e:
                    print(f"Error processing image '{img_path}': {e}")

    if num_images == 0:
        print("No image files found in the directory.")
        return

    average_height = total_height / num_images
    average_width = total_width / num_images

    return average_height, average_width

def mode_images_size(dataset_dir: str):

    '''
    Function that takes the dataset directory as input and returns the average height, width, mode height, mode width.
    '''
    heights = []
    widths = []
    num_images = 0

    for root, _, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path).convert('RGB')
                    width, height = img.size
                    heights.append(height)
                    widths.append(width)
                    num_images += 1

                except Exception as e:
                    print(f"Error processing image '{img_path}': {e}")

    if num_images == 0:
        print("No image files found in the directory.")
        return 0, 0

    mode_height = Counter(heights).most_common(1)[0][0]
    mode_width = Counter(widths).most_common(1)[0][0]

    return mode_height, mode_width


def compute_mean_std(dataset_dir, stats_file):
    heights = []
    widths = []
    total_height = 0
    total_width = 0
    num_images = 0

    pixel_sum = np.zeros(3)
    pixel_squared_sum = np.zeros(3)
    total_pixels = 0

    for root, _, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path).convert('RGB')
                    width, height = img.size
                    np_img = np.array(img) / 255.0  # Normalize pixel values to [0, 1]

                    heights.append(height)
                    widths.append(width)

                    total_height += height
                    total_width += width
                    num_images += 1

                    pixel_sum += np_img.sum(axis=(0, 1))
                    pixel_squared_sum += (np_img ** 2).sum(axis=(0, 1))
                    total_pixels += height * width

                except Exception as e:
                    print(f"Error processing image '{img_path}': {e}")

    if num_images == 0:
        print("No image files found in the directory.")
        return

    mean = pixel_sum / total_pixels
    std = np.sqrt(pixel_squared_sum / total_pixels - mean ** 2)

    statistics = {
        "mean": mean.tolist(),  
        "std": std.tolist()
    }

    with open(stats_file, 'w') as json_file:
        json.dump(statistics, json_file)