import React, { useState } from 'react';
import { api } from '../api';

export default function ExplainTab({ document, userLevel = 'MCA Student' }) {
  const [selectedLevel, setSelectedLevel] = useState(userLevel);
  const [concept, setConcept] = useState('');
  const [explanation, setExplanation] = useState('');
  const [loading, setLoading] = useState(false);

  const levels = [
    { id: 'Beginner', title: '🐣 Beginner', desc: 'Simple analogies & ELI5' },
    { id: 'Undergraduate', title: '🎓 Undergraduate', desc: 'Core principles & formulas' },
    { id: 'MCA Student', title: '💻 MCA Student', desc: 'Architecture & code tradeoffs' },
    { id: 'Researcher', title: '🔬 Researcher', desc: 'Mathematical rigor & theory' }
  ];

  const handleExplain = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    try {
      const res = await api.getExplanation(document.id, concept || document.title, selectedLevel);
      setExplanation(res.explanation);
    } catch (err) {
      alert(`Explain Mode failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const renderMarkdown = (text) => {
    if (window.marked) {
      return { __html: window.marked.parse(text) };
    }
    return { __html: text.replace(/\n/g, '<br/>') };
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ marginBottom: '16px' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '4px' }}>
            ⭐ AI Explain Mode (Adaptive Complexity Engine)
          </h2>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
            Get tailored explanations of research concepts customized to your target knowledge depth.
          </p>
        </div>

        {/* Level Selection Pills */}
        <div className="level-pills">
          {levels.map((lvl) => (
            <div
              key={lvl.id}
              className={`level-pill ${selectedLevel === lvl.id ? 'active' : ''}`}
              onClick={() => setSelectedLevel(lvl.id)}
            >
              <div>{lvl.title}</div>
              <div style={{ fontSize: '0.7rem', opacity: 0.75, marginTop: '2px' }}>{lvl.desc}</div>
            </div>
          ))}
        </div>

        <form onSubmit={handleExplain} style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            className="glass-input"
            style={{ flex: 1 }}
            placeholder={`Enter concept from "${document.title}" to explain (or leave blank for full paper concept)...`}
            value={concept}
            onChange={(e) => setConcept(e.target.value)}
          />
          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? '🧠 Explaining...' : '⚡ Explain Concept'}
          </button>
        </form>
      </div>

      {explanation && (
        <div className="glass-panel" style={{ padding: '28px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid var(--border-glass)', paddingBottom: '12px' }}>
            <span style={{ fontWeight: 700, fontSize: '1rem', color: '#f8fafc' }}>
              💡 Explanation Breakdown
            </span>
            <span className="badge badge-indigo">{selectedLevel} Mode</span>
          </div>
          <div className="md-output" dangerouslySetInnerHTML={renderMarkdown(explanation)} />
        </div>
      )}
    </div>
  );
}
