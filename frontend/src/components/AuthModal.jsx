import React, { useState } from 'react';
import { api } from '../api';

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [researchInterests, setResearchInterests] = useState('');
  const [academicLevel, setAcademicLevel] = useState('MCA Student');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let user;
      if (isRegister) {
        user = await api.register({
          username,
          email,
          password,
          research_interests: researchInterests,
          academic_level: academicLevel
        });
      } else {
        user = await api.login(username, password);
      }
      onAuthSuccess(user);
      onClose();
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="glass-panel modal-content">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>
            {isRegister ? '🚀 Join ScholarPulse AI' : '🔐 Welcome Back'}
          </h2>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '1.2rem', cursor: 'pointer' }}
          >
            ✕
          </button>
        </div>

        {error && (
          <div style={{ padding: '10px 14px', borderRadius: '8px', background: 'rgba(244, 63, 94, 0.15)', border: '1px solid rgba(244, 63, 94, 0.3)', color: '#fda4af', marginBottom: '16px', fontSize: '0.85rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px' }}>Username</label>
            <input
              type="text"
              className="glass-input"
              style={{ width: '100%' }}
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. rintathomas"
            />
          </div>

          {isRegister && (
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px' }}>Email Address</label>
              <input
                type="email"
                className="glass-input"
                style={{ width: '100%' }}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@university.edu"
              />
            </div>
          )}

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px' }}>Password</label>
            <input
              type="password"
              className="glass-input"
              style={{ width: '100%' }}
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          {isRegister && (
            <>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px' }}>Academic Level</label>
                <select
                  className="glass-input"
                  style={{ width: '100%' }}
                  value={academicLevel}
                  onChange={(e) => setAcademicLevel(e.target.value)}
                >
                  <option value="Beginner" style={{ background: '#0f172a' }}>Beginner</option>
                  <option value="Undergraduate" style={{ background: '#0f172a' }}>Undergraduate</option>
                  <option value="MCA Student" style={{ background: '#0f172a' }}>MCA Student</option>
                  <option value="Researcher" style={{ background: '#0f172a' }}>Researcher</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px' }}>Research Interests</label>
                <textarea
                  className="glass-input"
                  style={{ width: '100%', minHeight: '60px' }}
                  value={researchInterests}
                  onChange={(e) => setResearchInterests(e.target.value)}
                  placeholder="e.g. LLM RAG, Vector Search, Distributed Systems, Graph Neural Networks..."
                />
              </div>
            </>
          )}

          <button className="btn-primary" type="submit" disabled={loading} style={{ width: '100%', justifyContent: 'center', marginTop: '10px' }}>
            {loading ? 'Processing...' : isRegister ? 'Create Scholar Profile' : 'Sign In to Workspace'}
          </button>
        </form>

        <div style={{ marginTop: '20px', textAlign: 'center', fontSize: '0.85rem', color: '#94a3b8' }}>
          {isRegister ? 'Already registered?' : "Don't have a profile yet?"}{' '}
          <span
            style={{ color: '#6366f1', fontWeight: 600, cursor: 'pointer' }}
            onClick={() => { setIsRegister(!isRegister); setError(''); }}
          >
            {isRegister ? 'Sign In' : 'Create an Account'}
          </span>
        </div>
      </div>
    </div>
  );
}
