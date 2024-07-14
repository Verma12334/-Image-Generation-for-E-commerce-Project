import os
import requests
from tqdm import tqdm

# Define directories
product_dir = 'product_image_augmentation/dataset'
virtual_tryon_dir = 'virtual_tryon/static/uploads'

# Create directories if they don't exist
os.makedirs(product_dir, exist_ok=True)
os.makedirs(virtual_tryon_dir, exist_ok=True)

# Sample URLs for product images
product_images = [
    'https://unsplash.com/photos/Jztmx9yqjBw/download?force=true',
    'https://unsplash.com/photos/UOwvwZ9Dy6w/download?force=true'
]

# Sample URLs for model and apparel images
model_images = [
    'https://unsplash.com/photos/FV_PxCqgtwc/download?force=true'
]

apparel_images = [
    'https://unsplash.com/photos/ZGOTzTCNpdc/download?force=true'
]

# Function to download images
def download_images(image_urls, save_dir, prefix):
    for i, url in enumerate(tqdm(image_urls)):
        response = requests.get(url)
        with open(os.path.join(save_dir, f'{prefix}{i + 1}.jpg'), 'wb') as f:
            f.write(response.content)

# Download product images
download_images(product_images, product_dir, 'product')

# Download model and apparel images
download_images(model_images, virtual_tryon_dir, 'model')
download_images(apparel_images, virtual_tryon_dir, 'apparel')

print("Dataset download complete.")
