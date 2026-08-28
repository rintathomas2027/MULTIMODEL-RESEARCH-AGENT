import React, { useState } from 'react';
import { api } from '../api';

const PRESET_AVATARS = [
  { id: 'technomancer', label: 'Technomancer', icon: '🧙‍♂️', color: 'linear-gradient(135deg, #a78bfa, #7c3aed)' },
  { id: 'quantum', label: 'Quantum Pioneer', icon: '⚛️', color: 'linear-gradient(135deg, #22d3ee, #0891b2)' },
  { id: 'neural', label: 'Neural Nexus', icon: '🧠', color: 'linear-gradient(135deg, #f472b6, #db2777)' },
  { id: 'deepspace', label: 'Space Voyager', icon: '🚀', color: 'linear-gradient(135deg, #818cf8, #4f46e5)' },
  { id: 'genomic', label: 'Gene Explorer', icon: '🧬', color: 'linear-gradient(135deg, #34d399, #059669)' },
  { id: 'summa', label: 'Scholar Laureate', icon: '🎓', color: 'linear-gradient(135deg, #fbbf24, #d97706)' },
  { id: 'terminal', label: 'System Wizard', icon: '💻', color: 'linear-gradient(135deg, #10b981, #047857)' },
  { id: 'astro', label: 'Astrophysicist', icon: '🪐', color: 'linear-gradient(135deg, #f87171, #dc2626)' }
];

export default function ProfileModal({ isOpen, onClose, user, onUpdateUser }) {
  const profile = user?.profile || {};
  const [researchInterests, setResearchInterests] = useState(profile.research_interests || '');
  const [academicLevel, setAcademicLevel] = useState(profile.academic_level || 'MCA Student');
  const [avatar, setAvatar] = useState(profile.avatar || 'technomancer');
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState('');

  if (!isOpen || !user) return null;

  const currentAvatar = PRESET_AVATARS.find(av => av.id === avatar) || PRESET_AVATARS[0];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMsg('');

    try {
      const updatedUser = await api.updateProfile({
        research_interests: researchInterests,
        academic_level: academicLevel,
        avatar: avatar
      });
      onUpdateUser(updatedUser);
      setMsg('✅ Profile updated successfully!');
      setTimeout(() => setMsg(''), 2500);
    } catch (err) {
      alert(`Update failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="glass-panel modal-content" style={{ maxWidth: '540px', padding: '28px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f8fafc' }}>
            👤 Scholar Profile & Identity
          </h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '1.2rem', cursor: 'pointer' }}>✕</button>
        </div>

        {msg && (
          <div style={{ padding: '10px 14px', borderRadius: '8px', background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', color: '#6ee7b7', marginBottom: '16px', fontSize: '0.85rem' }}>
            {msg}
          </div>
        )}

        {/* Selected Avatar Large Display */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
          padding: '16px',
          borderRadius: '12px',
          background: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid var(--border-gold)',
          marginBottom: '20px'
        }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            background: currentAvatar.color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '2rem',
            boxShadow: '0 4px 15px rgba(0, 0, 0, 0.3)'
          }}>
            {currentAvatar.icon}
          </div>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc' }}>@{user.username}</h3>
            <p style={{ fontSize: '0.8rem', color: '#a5b4fc', marginTop: '2px', fontWeight: 600 }}>
              🎓 {academicLevel} • {currentAvatar.label} Theme
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Avatar Presets Picker */}
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '8px', fontWeight: 600 }}>
              Choose Scholar Avatar Preset
            </label>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '10px',
              maxHeight: '180px',
              overflowY: 'auto',
              padding: '4px'
            }}>
              {PRESET_AVATARS.map((av) => {
                const isSelected = av.id === avatar;
                return (
                  <button
                    key={av.id}
                    type="button"
                    onClick={() => setAvatar(av.id)}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      padding: '10px 4px',
                      borderRadius: '10px',
                      background: isSelected ? 'rgba(212, 175, 55, 0.15)' : 'rgba(255, 255, 255, 0.02)',
                      border: isSelected ? '2px solid var(--gold-main)' : '1px solid rgba(255, 255, 255, 0.05)',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                      boxShadow: isSelected ? '0 0 10px rgba(212, 175, 55, 0.25)' : 'none'
                    }}
                  >
                    <div style={{
                      width: '36px',
                      height: '36px',
                      borderRadius: '50%',
                      background: av.color,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '1.25rem',
                      marginBottom: '6px'
                    }}>
                      {av.icon}
                    </div>
                    <span style={{ fontSize: '0.7rem', color: isSelected ? '#f8fafc' : '#94a3b8', fontWeight: isSelected ? 700 : 500, textAlign: 'center', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', width: '100%' }}>
                      {av.label}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>Academic Level</label>
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
            <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>Research Interests & Focus</label>
            <textarea
              className="glass-input"
              style={{ width: '100%', minHeight: '80px', lineHeight: '1.4' }}
              value={researchInterests}
              onChange={(e) => setResearchInterests(e.target.value)}
              placeholder="e.g. Distributed Consensus, RAG Vector Indexes, Multimodal LLMs, NLP..."
            />
          </div>

          <button className="btn-primary" type="submit" disabled={loading} style={{ width: '100%', justifyContent: 'center', marginTop: '6px', padding: '10px 16px' }}>
            {loading ? 'Saving Changes...' : '💾 Save Profile & Avatar'}
          </button>
        </form>
      </div>
    </div>
  );
}
