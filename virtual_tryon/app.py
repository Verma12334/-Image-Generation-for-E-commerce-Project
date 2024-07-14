from flask import Flask, request, render_template, send_from_directory
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import os

app = Flask(__name__)

# Define image transformations
transform = transforms.Compose([
    transforms.Resize((256, 192)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

def load_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    return image

def virtual_try_on(model_image_path, apparel_image_path):
    model_image = load_image(model_image_path)
    apparel_image = load_image(apparel_image_path)

    # Simple blending algorithm for demo purposes
    output_image = model_image * 0.6 + apparel_image * 0.4
    output_image = output_image.squeeze(0).permute(1, 2, 0).numpy()
    output_image = (output_image * 255).astype(np.uint8)

    output_path = 'static/output/output_image.jpg'
    cv2.imwrite(output_path, cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))

    return output_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tryon', methods=['POST'])
def try_on():
    model_image = request.files['model_image']
    apparel_image = request.files['apparel_image']

    model_image_path = os.path.join('static/uploads', model_image.filename)
    apparel_image_path = os.path.join('static/uploads', apparel_image.filename)

    model_image.save(model_image_path)
    apparel_image.save(apparel_image_path)

    output_image_path = virtual_try_on(model_image_path, apparel_image_path)
    
    return send_from_directory('static/output', 'output_image.jpg')

if __name__ == '__main__':
    app.run(debug=True)
