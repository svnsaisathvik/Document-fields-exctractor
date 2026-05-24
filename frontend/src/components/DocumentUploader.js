import React, { useRef } from 'react';
import './DocumentUploader.css';

function DocumentUploader({ onUpload, loading }) {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = React.useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      validateAndUpload(files[0]);
    }
  };

  const handleInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndUpload(e.target.files[0]);
    }
  };

  const validateAndUpload = (file) => {
    const acceptedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    
    if (!acceptedTypes.includes(file.type)) {
      alert('Please upload an image (JPG/PNG) or PDF document');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB');
      return;
    }

    onUpload(file);
  };

  return (
    <div className="uploader-container">
      <h2>Upload Document</h2>
      
      <div
        className={`drag-drop-zone ${dragActive ? 'active' : ''} ${loading ? 'disabled' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => !loading && fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*,.pdf"
          onChange={handleInputChange}
          disabled={loading}
          style={{ display: 'none' }}
        />
        
        <div className="upload-icon">📤</div>
        <h3>Drag & Drop Your Document</h3>
        <p>or click to browse</p>
        <p className="file-types">Supported: JPG, PNG, PDF (Max 10MB)</p>
      </div>

      <div className="upload-tips">
        <h4>💡 Tips for best results:</h4>
        <ul>
          <li>Ensure document is clearly visible and well-lit</li>
          <li>Keep document straight and in focus</li>
          <li>Avoid shadows and glare on the document</li>
          <li>Support common document types: ID, Invoice, Passport, etc.</li>
        </ul>
      </div>
    </div>
  );
}

export default DocumentUploader;
