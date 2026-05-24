import React from 'react';
import './ExtractedFieldsDisplay.css';

function ExtractedFieldsDisplay({ data }) {
  const fields = data?.fields || {};

  return (
    <div className="fields-display-container">
      <h3>Extracted Fields</h3>

      {Object.keys(fields).length > 0 ? (
        <div className="fields-grid">
          {Object.entries(fields).map(([key, value], index) => (
            <div key={index} className="field-item">
              <div className="field-label">{key}</div>
              <div className="field-value">{value || 'N/A'}</div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-fields">
          <p>No fields extracted. Try uploading a clearer document.</p>
        </div>
      )}

      {data.raw_text && (
        <div className="raw-text-section">
          <h4>Raw Extracted Text</h4>
          <div className="raw-text-box">
            {data.raw_text}
          </div>
        </div>
      )}

      {fields.document_type && (
        <div className="document-info">
          <span className="info-badge">
            Document Type: <strong>{fields.document_type}</strong>
          </span>
        </div>
      )}

      {data.processing_time && (
        <div className="processing-time">
          ⏱️ Processing time: {data.processing_time}ms
        </div>
      )}
    </div>
  );
}

export default ExtractedFieldsDisplay;