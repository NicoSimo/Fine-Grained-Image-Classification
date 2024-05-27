import os
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt

def resize_with_padding(dataset_dir: str, output_dir: str, target_width, target_height) -> None:
    '''
    Function to resize all images in the dataset_dir while preserving aspect ratio and adding padding to fit the target dimensions.
    
    dataset_dir = Input the directory where the images are stored
    output_dir = Input the directory where the cropped images will be stored
    target width = Input the target width of the image
    target height = Input the target height of the image
    '''
    os.makedirs(output_dir, exist_ok=True)
    for root, dirs, files in os.walk(dataset_dir):
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
                crop_box = (0, 0, new_width, int(new_height * 0.98))  # NECESSARY TO CROP OUT THE BANNER

                # Crop the image to remove the copyright banner
                cropped_img = resized_img.crop(crop_box)

                # Create a new blank image with the target dimensions
                padded_img = Image.new("RGB", (target_width, target_height), color="black")

                # Calculate the position to paste the cropped image to center it with padding
                paste_x = (target_width - new_width) // 2
                paste_y = (target_height - cropped_img.size[1]) // 2

                # Paste the cropped image onto the blank image with padding
                padded_img.paste(cropped_img, (paste_x, paste_y))

                output_file = os.path.splitext(file)[0] + '_padded.jpg'
                output_path = os.path.join(output_dir, output_file)

                padded_img.save(output_path)

def images_sizes(dataset_dir: str):

    total_height = 0
    total_width = 0
    num_images = 0

    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path)
                    width, height = img.size

                    total_height += height
                    total_width += width
                    num_images += 1
                except Exception as e:
                    print(f"Error processing image '{img_path}': {e}")

    if num_images == 0:
        print("No image files found in the directory.")
        return 0, 0

    print(f'Total Height: {total_height}')
    print(f'Total Width: {total_width}')

    average_height = total_height / num_images
    average_width = total_width / num_images

    return average_height, average_width


def plot_image_size_distribution(dataset_dir: str):
    heights = []
    widths = []

    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path)
                    width, height = img.size
                    heights.append(height)
                    widths.append(width)
                except Exception as e:
                    print(f"Error processing image '{img_path}': {e}")

    if not heights or not widths:
        print("No image files found in the directory.")
        return

    # Plot distribution of heights
    plt.figure(figsize=(10, 5))
    plt.hist(heights, bins=30, color='blue', alpha=0.7)
    plt.title('Distribution of Image Heights')
    plt.xlabel('Height')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # Plot distribution of widths
    plt.figure(figsize=(10, 5))
    plt.hist(widths, bins=30, color='red', alpha=0.7)
    plt.title('Distribution of Image Widths')
    plt.xlabel('Width')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

dataset_dir = '/Users/nicolosimonato/Desktop/UNITRENTO/IntroToML/MLCompetition/data/flowers-102/jpg'
plot_image_size_distribution(dataset_dir)
