from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from PIL import Image
import io
import base64
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import os

app = Flask(__name__)
CORS(app)

# Initialize model components
print("Loading model components...")
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
print(f"Using device: {device}")

braille_dict = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
    ' ': ' ', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙',
    '5': '⠼⠑', '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚'
}

def text_to_braille(text):
    return ''.join(braille_dict.get(char.lower(), '?') for char in text)

@app.route("/generate", methods=["POST"])
def generate_caption_and_braille():
    try:
        image_data = request.json.get("image")
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        # Remove the data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert image to RGB if it's not
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image if it's too large
            max_size = 800
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)

        except Exception as e:
            return jsonify({"error": f"Invalid image data: {str(e)}"}), 400

        # Process the image
        inputs = processor(images=image, return_tensors="pt").pixel_values
        inputs = inputs.to(device)

        # Generate caption
        outputs = model.generate(
            inputs,
            max_length=50,
            num_beams=5,
            temperature=1.0,
            do_sample=True,
            top_p=0.9
        )
        caption = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Convert to braille
        braille_text = text_to_braille(caption)

        return jsonify({
            "caption": caption,
            "braille": braille_text
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
