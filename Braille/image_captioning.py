import torch
from PIL import Image
import pickle
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import os

def initialize_model():
    # Initialize the model components
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    return model, processor, tokenizer, device

def generate_caption(image_path, model, processor, tokenizer, device):
    # Load and preprocess the image
    image = Image.open(image_path).convert('RGB')
    
    # Process the image
    inputs = processor(images=image, return_tensors="pt").pixel_values
    inputs = inputs.to(device)
    
    # Generate caption
    outputs = model.generate(inputs, max_length=50, num_beams=5)
    caption = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return caption

def main():
    # Initialize model
    print("Initializing model...")
    model, processor, tokenizer, device = initialize_model()
    print(f"Using device: {device}")

    # Test images
    test_images = ['imgg1.jpg', 'imgg2.jpg', 'imgg3.jpg']

    for img_path in test_images:
        if os.path.exists(img_path):
            print(f'\nProcessing image: {img_path}')
            caption = generate_caption(img_path, model, processor, tokenizer, device)
            print(f'Generated Caption: {caption}')
            print('-' * 50)

if __name__ == "__main__":
    main() 