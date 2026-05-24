import React, { useState } from 'react';
import './App.css';
import DocumentUploader from './components/DocumentUploader';
import ExtractedFieldsDisplay from './components/ExtractedFieldsDisplay';

function App() {
  const [extractedData, setExtractedData] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDocumentUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    try {
      // Create preview of uploaded image
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
      };
      reader.readAsDataURL(file);

      // Send to backend for OCR processing
      const formData = new FormData();
      formData.append('image', file);

      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/extract`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Failed to extract fields from document');
      }

      const data = await response.json();
      setExtractedData(data);
      setError(null);
    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
      setExtractedData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="app-header">
        <h1>📄 OCR Document Field Extraction</h1>
        <p>Upload your document to automatically extract and display fields</p>
      </div>

      <div className="app-content">
        <div className="uploader-section">
          <DocumentUploader onUpload={handleDocumentUpload} loading={loading} />
        </div>

        <div className="results-section">
          {uploadedImage && (
            <div className="image-preview">
              <h3>Uploaded Document</h3>
              <img src={uploadedImage} alt="Uploaded document" />
            </div>
          )}

          {loading && (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>Processing document with OCR...</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {extractedData && !loading && (
            <ExtractedFieldsDisplay data={extractedData} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
