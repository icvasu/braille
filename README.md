# Braille Image Captioning Project

This project provides an AI-powered system that generates image captions and converts them to Braille representation. It consists of a React frontend and a Flask backend that uses the VIT-GPT2 model for image captioning.

## Features

- Image upload and preview
- AI-powered image captioning
- Automatic Braille conversion
- Modern, responsive UI
- Real-time processing

## Project Structure

```
braille/
├── backend/               # Flask server
│   ├── app.py            # Main server file
│   ├── requirements.txt  # Python dependencies
│   └── Procfile         # For deployment
├── frontend/             # React frontend
│   └── braille_summarization/
│       ├── src/         # Source code
│       ├── public/      # Public assets
│       └── package.json # Node dependencies
```

## Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

## Installation

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Download the model files:
   The model files are too large for GitHub. You need to download them using the transformers library:
   ```python
   from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
   
   model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
   processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
   tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend/braille_summarization
   npm install
   ```

## Running Locally

1. Start the backend server:
   ```bash
   cd backend
   python app.py
   ```
   The server will run on http://localhost:5000

2. Start the frontend development server:
   ```bash
   cd frontend/braille_summarization
   npm run dev
   ```
   The frontend will run on http://localhost:5173

## Deployment

### Frontend (Vercel)

1. Push your code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import your repository
4. Configure:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Add Environment Variables:
   - `VITE_API_URL`: Your backend URL

### Backend (Render)

1. Go to [Render](https://render.com)
2. Create a new Web Service
3. Connect your repository
4. Configure:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add Environment Variables:
   - `PYTHON_VERSION`: `3.9.0`
   - `PORT`: `10000`

## Contributing

Feel free to open issues and pull requests!

## License

MIT License 