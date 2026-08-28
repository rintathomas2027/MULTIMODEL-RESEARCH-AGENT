import React, { useState } from 'react';
import { api } from '../api';

export default function UploadModal({ isOpen, onClose, onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      if (!title) {
        setTitle(selected.name.replace(/\.[^/.]+$/, ''));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF, DOCX, PPTX, or TXT file.');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const doc = await api.uploadDocument(file, title);
      onUploadSuccess(doc);
      onClose();
      setFile(null);
      setTitle('');
    } catch (err) {
      setError(err.message || 'File upload and processing failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="glass-panel modal-content" style={{ maxWidth: '520px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '1.3rem', fontWeight: 800 }}>📤 Upload Research Paper</h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '1.2rem', cursor: 'pointer' }}>✕</button>
        </div>

        {error && (
          <div style={{ padding: '10px 14px', borderRadius: '8px', background: 'rgba(244, 63, 94, 0.15)', border: '1px solid rgba(244, 63, 94, 0.3)', color: '#fda4af', marginBottom: '16px', fontSize: '0.85rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px' }}>Document Title</label>
            <input
              type="text"
              className="glass-input"
              style={{ width: '100%' }}
              placeholder="e.g. Deep Residual Learning for Image Recognition"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          <div
            style={{
              border: '2px dashed rgba(99, 102, 241, 0.4)',
              borderRadius: '12px',
              padding: '32px 20px',
              textAlign: 'center',
              background: 'rgba(15, 23, 42, 0.4)',
              cursor: 'pointer'
            }}
            onClick={() => document.getElementById('paperFileInput').click()}
          >
            <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>📄</div>
            <p style={{ fontWeight: 600, fontSize: '0.95rem', marginBottom: '4px' }}>
              {file ? file.name : 'Click or Drag & Drop File'}
            </p>
            <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
              Supports PDF, DOCX, PPTX, TXT files (Max 50MB)
            </p>
            <input
              id="paperFileInput"
              type="file"
              accept=".pdf,.docx,.doc,.pptx,.ppt,.txt,.md"
              style={{ display: 'none' }}
              onChange={handleFileChange}
            />
          </div>

          <button className="btn-primary" type="submit" disabled={loading || !file} style={{ width: '100%', justifyContent: 'center', marginTop: '10px' }}>
            {loading ? '🧠 Processing Text & Vector Embeddings...' : '⚡ Process & Index Document'}
          </button>
        </form>
      </div>
    </div>
  );
}
