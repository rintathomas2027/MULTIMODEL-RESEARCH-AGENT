import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import AuthModal from './components/AuthModal';
import Workspace from './components/Workspace';
import DocumentStudio from './components/DocumentStudio';
import ProfileModal from './components/ProfileModal';
import UploadModal from './components/UploadModal';
import { api } from './api';

export default function App() {
  const [user, setUser] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [search, setSearch] = useState('');
  const [loadingDocs, setLoadingDocs] = useState(false);

  // Modals
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);

  useEffect(() => {
    // Check initial user from localStorage or fetch profile
    const savedUser = localStorage.getItem('sp_user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        loadDocuments();
      } catch (e) {
        localStorage.removeItem('sp_user');
      }
    }

    const handleAuthExpired = () => {
      setUser(null);
      setDocuments([]);
      setSelectedDoc(null);
      setShowAuthModal(true);
    };

    window.addEventListener('auth_expired', handleAuthExpired);
    return () => window.removeEventListener('auth_expired', handleAuthExpired);
  }, []);

  useEffect(() => {
    if (user) {
      loadDocuments(search);
    }
  }, [search, user]);

  const loadDocuments = async (query = '') => {
    setLoadingDocs(true);
    try {
      const docs = await api.getDocuments(query);
      setDocuments(docs);
    } catch (err) {
      console.error('Failed to load documents:', err);
    } finally {
      setLoadingDocs(false);
    }
  };

  const handleAuthSuccess = (userData) => {
    setUser(userData);
    loadDocuments();
  };

  const handleLogout = () => {
    api.clearTokens();
    setUser(null);
    setDocuments([]);
    setSelectedDoc(null);
  };

  const handleUploadSuccess = (newDoc) => {
    setDocuments(prev => [newDoc, ...prev]);
    setSelectedDoc(newDoc);
  };

  const handleDeleteDoc = async (docId) => {
    try {
      await api.deleteDocument(docId);
      setDocuments(prev => prev.filter(d => d.id !== docId));
      if (selectedDoc && selectedDoc.id === docId) {
        setSelectedDoc(null);
      }
    } catch (err) {
      alert(`Failed to delete document: ${err.message}`);
    }
  };

  return (
    <div className="app-container">
      <Navbar
        user={user}
        search={search}
        setSearch={setSearch}
        onOpenAuth={() => setShowAuthModal(true)}
        onOpenProfile={() => setShowProfileModal(true)}
        onOpenUpload={() => setShowUploadModal(true)}
        onLogout={handleLogout}
      />

      <main className="main-content">
        {!user ? (
          /* Landing Screen when unauthenticated */
          <div className="glass-panel" style={{ padding: '64px 32px', textAlign: 'center', marginTop: '40px', maxWidth: '800px', margin: '40px auto 0 auto' }}>
            <div className="brand-icon" style={{ width: '64px', height: '64px', fontSize: '2rem', margin: '0 auto 20px auto' }}>⚡</div>
            <h1 style={{ fontSize: '2.4rem', fontWeight: 800, marginBottom: '14px', lineHeight: '1.2' }}>
              ScholarPulse AI
            </h1>
            <p style={{ fontSize: '1.1rem', color: '#94a3b8', maxWidth: '600px', margin: '0 auto 28px auto', lineHeight: '1.6' }}>
              An Intelligent Collaborative Multimodal Research Assistant powered by LLMs and Retrieval-Augmented Generation (RAG).
            </p>

            <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', flexWrap: 'wrap', marginBottom: '40px' }}>
              <div className="badge badge-indigo" style={{ padding: '8px 16px', fontSize: '0.85rem' }}>📄 Multi-Format RAG (PDF/DOCX/PPTX)</div>
              <div className="badge badge-teal" style={{ padding: '8px 16px', fontSize: '0.85rem' }}>⭐ Adaptive 4-Level Explain Mode</div>
              <div className="badge badge-amber" style={{ padding: '8px 16px', fontSize: '0.85rem' }}>📊 AI Presentation Slide Generator</div>
              <div className="badge badge-cyan" style={{ padding: '8px 16px', fontSize: '0.85rem' }}>🎓 Viva Defense & Exam Prep</div>
            </div>

            <button className="btn-primary" style={{ padding: '14px 36px', fontSize: '1.05rem' }} onClick={() => setShowAuthModal(true)}>
              🚀 Get Started & Access Workspace
            </button>
          </div>
        ) : (
          /* Main Workspace View */
          <div>
            {!selectedDoc ? (
              <Workspace
                documents={documents}
                selectedDoc={selectedDoc}
                onSelectDoc={(doc) => setSelectedDoc(doc)}
                onDeleteDoc={handleDeleteDoc}
                onOpenUpload={() => setShowUploadModal(true)}
                loading={loadingDocs}
              />
            ) : (
              <DocumentStudio
                document={selectedDoc}
                userLevel={user?.profile?.academic_level || 'MCA Student'}
                onCloseDoc={() => setSelectedDoc(null)}
              />
            )}
          </div>
        )}
      </main>

      {/* Modals */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onAuthSuccess={handleAuthSuccess}
      />

      <ProfileModal
        isOpen={showProfileModal}
        onClose={() => setShowProfileModal(false)}
        user={user}
        onUpdateUser={(updated) => setUser(updated)}
      />

      <UploadModal
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        onUploadSuccess={handleUploadSuccess}
      />
    </div>
  );
}
