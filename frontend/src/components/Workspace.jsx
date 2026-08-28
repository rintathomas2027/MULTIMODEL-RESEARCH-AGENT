import React, { useState } from 'react';

export default function Workspace({ documents, selectedDoc, onSelectDoc, onDeleteDoc, onOpenUpload, loading }) {
  const getFileBadge = (file) => {
    if (!file) return <span className="badge badge-indigo">PDF</span>;
    if (file.endsWith('.pdf')) return <span className="badge badge-indigo">PDF</span>;
    if (file.endsWith('.docx') || file.endsWith('.doc')) return <span className="badge badge-teal">DOCX</span>;
    if (file.endsWith('.pptx') || file.endsWith('.ppt')) return <span className="badge badge-amber">PPTX</span>;
    return <span className="badge badge-cyan">TXT</span>;
  };

  return (
    <div style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>📂 Research Workspace</h2>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
            Select a document to open AI Assistant, Explain Mode, Presentation & Viva tools
          </p>
        </div>
        <button className="btn-primary" onClick={onOpenUpload}>
          ➕ Upload Document
        </button>
      </div>

      {loading ? (
        <div className="glass-panel" style={{ padding: '32px', textAlign: 'center', color: '#94a3b8' }}>
          ⏳ Loading research workspace...
        </div>
      ) : documents.length === 0 ? (
        <div className="glass-panel" style={{ padding: '48px', textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: '12px' }}>📄</div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '6px' }}>No Research Papers Uploaded</h3>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: '16px' }}>
            Upload your first research paper (PDF, DOCX, PPTX, or TXT) to get started.
          </p>
          <button className="btn-primary" onClick={onOpenUpload}>
            📤 Upload First Paper
          </button>
        </div>
      ) : (
        <div className="doc-grid">
          {documents.map((doc) => {
            const isSelected = selectedDoc && selectedDoc.id === doc.id;
            return (
              <div
                key={doc.id}
                className="glass-panel doc-card"
                style={{
                  borderColor: isSelected ? 'var(--gold-main)' : 'rgba(255, 255, 255, 0.08)',
                  background: isSelected ? 'rgba(184, 134, 11, 0.12)' : 'rgba(15, 23, 42, 0.75)',
                  boxShadow: isSelected ? '0 0 15px rgba(184, 134, 11, 0.15)' : 'none'
                }}
                onClick={() => onSelectDoc(doc)}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                    {getFileBadge(doc.file)}
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{doc.file_size_formatted}</span>
                  </div>

                  <h3
                    style={{
                      fontSize: '0.95rem',
                      fontWeight: 700,
                      color: '#f8fafc',
                      marginBottom: '8px',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden'
                    }}
                    title={doc.title}
                  >
                    {doc.title}
                  </h3>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '14px', paddingTop: '12px', borderTop: '1px solid rgba(255, 255, 255, 0.05)' }}>
                  <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    📅 {new Date(doc.uploaded_at).toLocaleDateString()}
                  </span>
                  <button
                    className="btn-secondary"
                    style={{ padding: '4px 8px', fontSize: '0.75rem', color: '#f43f5e' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      if (window.confirm(`Delete "${doc.title}"?`)) {
                        onDeleteDoc(doc.id);
                      }
                    }}
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
