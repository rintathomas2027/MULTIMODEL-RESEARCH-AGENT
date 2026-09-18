import React from 'react';

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

export default function Navbar({ user, onOpenAuth, onOpenProfile, onOpenUpload, onLogout, search, setSearch, showLandingPage, onToggleLanding }) {
  const profile = user?.profile || {};
  const avatarId = profile.avatar || 'technomancer';
  const currentAvatar = PRESET_AVATARS.find(av => av.id === avatarId) || PRESET_AVATARS[0];

  return (
    <nav className="navbar" style={{ borderBottom: '1px solid var(--border-gold)' }}>
      <div className="brand-logo" onClick={onToggleLanding} style={{ cursor: 'pointer' }} title="Go to Front Page">
        <div className="brand-icon" style={{ textShadow: '0 0 10px rgba(212,175,55,0.4)' }}>⚡</div>
        <div>
          <span style={{ fontWeight: 800, letterSpacing: '0.02em' }}>ScholarPulse</span>
          <span style={{ color: 'var(--gold-main)', marginLeft: '4px', fontWeight: 800 }}>AI</span>
        </div>
      </div>

      {user && !showLandingPage && (
        <div style={{ flex: 1, maxWidth: '400px', margin: '0 32px' }}>
          <input
            type="text"
            className="glass-input"
            style={{ width: '100%', borderRadius: '20px', padding: '8px 18px' }}
            placeholder="🔍 Search research papers & topics..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      )}

      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginLeft: 'auto' }}>
        {user ? (
          <>
            {onToggleLanding && (
              <button className="btn-secondary" onClick={onToggleLanding} style={{ padding: '8px 14px', borderRadius: '8px', fontSize: '0.85rem' }}>
                {showLandingPage ? '📚 Workspace' : '🏠 Front Page'}
              </button>
            )}

            {!showLandingPage && (
              <button className="btn-primary" onClick={onOpenUpload} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span>📤</span> Upload Paper
              </button>
            )}

            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                padding: '5px 12px',
                borderRadius: '20px',
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid var(--border-gold)',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
              onClick={onOpenProfile}
              title="Open Scholar Profile"
            >
              <div
                style={{
                  width: '34px',
                  height: '34px',
                  borderRadius: '50%',
                  background: currentAvatar.color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.1rem',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)'
                }}
              >
                {currentAvatar.icon}
              </div>
              <div style={{ textAlign: 'left', lineHeight: '1.2' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc' }}>{user.username}</div>
                <div className="badge" style={{ fontSize: '0.62rem', padding: '1px 6px', marginTop: '1px', background: 'rgba(212,175,55,0.15)', border: '1px solid var(--border-gold)', color: '#fbbf24' }}>
                  {profile.academic_level || 'MCA Student'}
                </div>
              </div>
            </div>

            <button className="btn-secondary" onClick={onLogout} title="Logout" style={{ padding: '8px 12px', borderRadius: '8px' }}>
              🚪 Logout
            </button>
          </>
        ) : (
          <button className="btn-primary" onClick={onOpenAuth}>
            🔒 Login / Register
          </button>
        )}
      </div>
    </nav>
  );
}
