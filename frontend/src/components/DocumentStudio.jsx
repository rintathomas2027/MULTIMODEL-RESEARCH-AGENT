import React, { useState } from 'react';
import ChatTab from './ChatTab';
import ExplainTab from './ExplainTab';
import PresentationTab from './PresentationTab';
import VivaTab from './VivaTab';
import FormulaTab from './FormulaTab';

export default function DocumentStudio({ document, userLevel, onCloseDoc }) {
  const [activeTab, setActiveTab] = useState('chat');

  if (!document) return null;

  return (
    <div style={{ marginTop: '24px' }}>
      {/* Studio Header Bar */}
      <div className="glass-panel" style={{ padding: '20px 24px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <button className="btn-secondary" onClick={onCloseDoc} title="Back to workspace">
            ← Back
          </button>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 800 }}>{document.title}</h2>
              <span className="badge badge-indigo">Active Paper</span>
            </div>
            <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginTop: '2px' }}>
              Uploaded on {new Date(document.uploaded_at).toLocaleDateString()} • {document.file_size_formatted}
            </p>
          </div>
        </div>

        <div style={{ fontSize: '0.82rem', color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span>🧠 Engine:</span>
          <strong>Gemini RAG + ChromaDB</strong>
        </div>
      </div>

      {/* Studio Tabs Navigation */}
      <div className="studio-nav">
        <button
          className={`studio-tab ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          💬 AI Research Assistant (RAG Chat)
        </button>

        <button
          className={`studio-tab ${activeTab === 'formula' ? 'active' : ''}`}
          onClick={() => setActiveTab('formula')}
        >
          🧮 Formula to Code
        </button>

        <button
          className={`studio-tab ${activeTab === 'explain' ? 'active' : ''}`}
          onClick={() => setActiveTab('explain')}
        >
          ⭐ AI Explain Mode (Multi-Level)
        </button>

        <button
          className={`studio-tab ${activeTab === 'presentation' ? 'active' : ''}`}
          onClick={() => setActiveTab('presentation')}
        >
          ⭐ AI Presentation Assistant
        </button>

        <button
          className={`studio-tab ${activeTab === 'viva' ? 'active' : ''}`}
          onClick={() => setActiveTab('viva')}
        >
          ⭐ AI Viva Generator
        </button>
      </div>

      {/* Active Tab View */}
      {activeTab === 'chat' && <ChatTab document={document} />}
      {activeTab === 'formula' && <FormulaTab document={document} />}
      {activeTab === 'explain' && <ExplainTab document={document} userLevel={userLevel} />}
      {activeTab === 'presentation' && <PresentationTab document={document} />}
      {activeTab === 'viva' && <VivaTab document={document} />}
    </div>
  );
}
