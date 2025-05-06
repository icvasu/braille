from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
import pickle

def setup_model():
    # Initialize the model components
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # Save model, processor, and tokenizer
    with open("oo.pkl", "wb") as f:
        pickle.dump({
            "model": model,
            "processor": processor,
            "tokenizer": tokenizer
        }, f)

    print("Model, processor, and tokenizer saved to 'oo.pkl'")
    return model, processor, tokenizer

if __name__ == "__main__":
    setup_model() 