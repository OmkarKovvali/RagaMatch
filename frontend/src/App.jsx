import { useState } from 'react'
import './App.css'
import logo from './assets/finale_logo.png';
import templeBg from './assets/redo_background.png';
// import mandala from './assets/Gemini_Generated_Image_jf3k7ojf3k7ojf3k-removebg-preview.png';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (selectedFile = file) => {
    if (!selectedFile) return;
    setLoading(true);
    console.log('Uploading file:', selectedFile.name);
    const formData = new FormData();
    formData.append('file', selectedFile);
    try {
      const res = await fetch('http://localhost:8000/predict/', { method: 'POST', body: formData });
      if (!res.ok) {
        console.error('Upload failed with status:', res.status);
        setLoading(false);
        return;
      }
      const prediction = await res.json();
      console.log('Prediction result from backend:', prediction);
      setResult(prediction.prediction);
    } catch (err) {
      console.error('Error during upload:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (selectedFile) {
      console.log('File selected:', selectedFile.name, selectedFile.size, selectedFile.type);
      handleUpload(selectedFile);
    }
  };

  return (
    <div className="hero" style={{ backgroundImage: `url(${templeBg})` }}>
      <header className="header">
        <img src={logo} alt="RagaMatch Logo" className="logo-img" />
        <button className="sign-in-btn">Sign In</button>
      </header>
      <main className="main-content">
        <h1 className="title">Classical Roots. <span className="modern">Modern Intelligence.</span></h1>
        <h2 className="subtitle">Identify Any Raga in <span className="seconds">Seconds.</span></h2>
        <div className="upload-section">
          <input
            type="file"
            accept="audio/*"
            id="file-upload"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          <label htmlFor="file-upload" className="upload-btn">
            {loading ? 'Identifying...' : 'Upload File'}
          </label>
        </div>
        {result && <div className="result">The Raga is <span className="raga-name">{result}</span></div>}
        {/* Mandala image removed as requested */}
      </main>
    </div>
  );
}

export default App;
