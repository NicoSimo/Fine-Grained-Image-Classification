import os
from PIL import Image

def resize_with_padding(dataset_dir: str, output_dir: str, target_width, target_height):
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

                # Get the original dimensions
                original_width, original_height = img.size

                # Calculate scaling factor for resizing
                scale_factor_width = target_width / original_width
                scale_factor_height = target_height / original_height
                scale_factor = min(scale_factor_width, scale_factor_height)

                # Resize the image while preserving aspect ratio
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                # Create a new blank image with the target dimensions
                padded_img = Image.new("RGB", (target_width, target_height), color="white")

                # Calculate the position to paste the resized image to center it with padding
                paste_x = (target_width - new_width) // 2
                paste_y = (target_height - new_height) // 2

                # Paste the resized image onto the blank image with padding
                padded_img.paste(resized_img, (paste_x, paste_y))

                output_file = os.path.splitext(file)[0] + '_padded.jpg'
                output_path = os.path.join(output_dir, output_file)

                padded_img.save(output_path)

def images_sizes(dataset_dir: str):
    '''
    Function to calculate the average height and width of images in a dataset. 
    It returns the average height and width of the images.
    
    dataset_dir = Input the directory where the images are stored
    '''
    total_height = 0
    total_width = 0
    num_images = 0

    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                img_path = os.path.join(root, file)
                img = Image.open(img_path)
                width, height = img.size

                total_height += height
                total_width += width
                num_images += 1

    average_height = total_height / num_images
    average_width = total_width / num_images

    return average_height, average_width