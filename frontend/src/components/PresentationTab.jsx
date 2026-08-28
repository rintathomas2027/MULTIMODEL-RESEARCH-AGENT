import React, { useState } from 'react';
import { api } from '../api';

export default function PresentationTab({ document }) {
  const [presentation, setPresentation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copiedSlide, setCopiedSlide] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await api.getPresentation(document.id);
      setPresentation(res);
    } catch (err) {
      alert(`Presentation generation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const copySlideText = (slide, index) => {
    const text = `Slide ${slide.slide_number}: ${slide.title}\n` +
      slide.bullets.map(b => `• ${b}`).join('\n') +
      (slide.speaker_notes ? `\n\nSpeaker Notes: ${slide.speaker_notes}` : '');
    navigator.clipboard.writeText(text);
    setCopiedSlide(index);
    setTimeout(() => setCopiedSlide(null), 2000);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="glass-panel" style={{ padding: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '4px' }}>
            ⭐ AI Presentation Assistant
          </h2>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
            Auto-generate professional presentation slide outlines (Intro, Objectives, Methodology, Results, Conclusion).
          </p>
        </div>
        <button className="btn-primary" onClick={handleGenerate} disabled={loading}>
          {loading ? '⚡ Generating Slides...' : presentation ? '🔄 Re-Generate Slides' : '📊 Generate Slide Deck'}
        </button>
      </div>

      {presentation && presentation.slides && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>
              📽️ Presentation Slides for "{presentation.title}"
            </h3>
            <span className="badge badge-teal">{presentation.slides.length} Slides Generated</span>
          </div>

          {presentation.slides.map((slide, idx) => (
            <div key={idx} className="glass-panel slide-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span className="badge badge-indigo">Slide {slide.slide_number || idx + 1}</span>
                  <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>{slide.title}</h4>
                </div>
                <button
                  className="btn-secondary"
                  style={{ fontSize: '0.78rem', padding: '4px 10px' }}
                  onClick={() => copySlideText(slide, idx)}
                >
                  {copiedSlide === idx ? '✅ Copied!' : '📋 Copy Slide'}
                </button>
              </div>

              <ul style={{ paddingLeft: '20px', marginBottom: '14px', color: '#cbd5e1', fontSize: '0.92rem' }}>
                {slide.bullets && slide.bullets.map((b, bIdx) => (
                  <li key={bIdx} style={{ marginBottom: '6px' }}>{b}</li>
                ))}
              </ul>

              {slide.speaker_notes && (
                <div
                  style={{
                    padding: '10px 14px',
                    borderRadius: '8px',
                    background: 'rgba(99, 102, 241, 0.1)',
                    border: '1px solid rgba(99, 102, 241, 0.2)',
                    fontSize: '0.82rem',
                    color: '#a5b4fc'
                  }}
                >
                  💬 <strong>Speaker Guidance:</strong> {slide.speaker_notes}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
