import os
from PIL import Image
import matplotlib.pyplot as plt

def plot_image_size_distribution(dataset_dir: str):
    '''
    Function that plots the MODE of the distribution of image sizes (heights and widths) in the dataset.
    '''
    heights = []
    widths = []

    for root, _, files in os.walk(dataset_dir):
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

    plt.figure(figsize=(10, 5))
    plt.hist(heights, bins=30, color='blue', alpha=0.7)
    plt.title('Distribution of Image Heights')
    plt.xlabel('Height')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.hist(widths, bins=30, color='red', alpha=0.7)
    plt.title('Distribution of Image Widths')
    plt.xlabel('Width')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()