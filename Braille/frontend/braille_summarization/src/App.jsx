import React, { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [caption, setCaption] = useState("");
  const [braille, setBraille] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError("Image size should be less than 5MB");
        return;
      }
      
      // Check file type
      if (!file.type.startsWith('image/')) {
        setError("Please upload an image file");
        return;
      }

      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        setImagePreview(reader.result);
        setError("");
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
    if (!image) {
      setError("Please upload an image!");
      return;
    }

    setError("");
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image }),
      });

      const data = await response.json();
      if (response.ok) {
        setCaption(data.caption);
        setBraille(data.braille);
      } else {
        setError(data.error || "Something went wrong!");
      }
    } catch (err) {
      setError("Failed to connect to the server! Please make sure the backend is running.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Image Summarization and Braille Conversion</h1>
        <p>Upload an image to generate its caption and Braille text representation.</p>
      </header>

      <main>
        <section className="upload-section">
          <div className="image-container">
            <h2>Upload Image</h2>
            <input 
              type="file" 
              accept="image/*" 
              onChange={handleImageChange}
              className="file-input" 
            />
            {imagePreview && (
              <div className="image-preview">
                <img src={imagePreview} alt="Uploaded Preview" />
              </div>
            )}
            <button 
              onClick={handleSubmit} 
              disabled={loading || !image}
              className={loading ? 'loading' : ''}
            >
              {loading ? 'Generating...' : 'Generate Caption'}
            </button>
          </div>

          <div className="output-container">
            {error && <div className="error">{error}</div>}
            {caption && (
              <>
                <h3>Generated Caption:</h3>
                <p className="caption">{caption}</p>
              </>
            )}
            {braille && (
              <>
                <h3>Braille Representation:</h3>
                <p className="braille">{braille}</p>
              </>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
