import React, { useState } from 'react';
import { api } from '../api';

export default function VivaTab({ document }) {
  const [vivaData, setVivaData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeCategory, setActiveCategory] = useState('all');
  const [expandedIndex, setExpandedIndex] = useState({});
  const [copiedKey, setCopiedKey] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await api.getVivaQuestions(document.id);
      setVivaData(res);
    } catch (err) {
      alert(`Viva questions generation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const toggleAnswer = (key) => {
    setExpandedIndex(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const copyToClipboard = (text, key) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const renderMarkdown = (text) => {
    if (window.marked) {
      return { __html: window.marked.parse(text) };
    }
    // simple paragraphing fallback
    return { __html: text.replace(/\n/g, '<br/>') };
  };

  // Helper to get defence strategies based on category
  const getDefenseTip = (category) => {
    if (category === '2mark') {
      return "🎓 **Viva Tip:** Keep this explanation concise. External examiners look for exact keywords and precise definitions. State the core concept first, followed by a direct example.";
    } else if (category === '5mark') {
      return "💡 **Viva Strategy:** Present this answer structurally. Always draw a neat flow block diagram or table schema on the board. Break it down into Core Architecture, System Flow, and Advantages.";
    } else {
      return "🔥 **Defense Shield:** Examiners ask this to check if you actually built the project yourself. Confidently defend your choices by discussing performance tradeoffs, constraints, and why alternative solutions (e.g. standard databases vs vector stores) were rejected.";
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header panel */}
      <div className="glass-panel" style={{
        padding: '24px 30px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderLeft: '5px solid var(--gold-main)',
        background: 'linear-gradient(90deg, rgba(212,175,55,0.05) 0%, rgba(15,23,42,0.9) 100%)'
      }}>
        <div>
          <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
            🎓 AI External Viva & Exam Defense Gateway
          </h2>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '4px' }}>
            Generate and master exhaustive 2-Mark, 5-Mark, and Tough External Defense Q&As with detailed model solutions.
          </p>
        </div>
        <button
          className="btn-primary"
          onClick={handleGenerate}
          disabled={loading}
          style={{ padding: '12px 28px', fontSize: '0.9rem', borderRadius: '24px', boxShadow: '0 0 15px rgba(212,175,55,0.2)' }}
        >
          {loading ? '⚡ Assembling Viva Deck...' : vivaData ? '🔄 Re-Generate Question Deck' : '🎓 Generate Viva Deck'}
        </button>
      </div>

      {vivaData && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
          {/* Category Filters */}
          <div style={{
            display: 'flex',
            gap: '10px',
            background: 'rgba(255, 255, 255, 0.02)',
            padding: '6px',
            borderRadius: '30px',
            border: '1px solid rgba(255, 255, 255, 0.05)',
            alignSelf: 'flex-start'
          }}>
            <button
              className={`level-pill ${activeCategory === 'all' ? 'active' : ''}`}
              onClick={() => setActiveCategory('all')}
              style={{ padding: '8px 20px', borderRadius: '20px' }}
            >
              All Questions ({ (vivaData.two_mark_questions?.length || 0) + (vivaData.five_mark_questions?.length || 0) + (vivaData.viva_questions?.length || 0) })
            </button>
            <button
              className={`level-pill ${activeCategory === '2mark' ? 'active' : ''}`}
              onClick={() => setActiveCategory('2mark')}
              style={{ padding: '8px 20px', borderRadius: '20px' }}
            >
              2-Mark Definition Qs ({vivaData.two_mark_questions?.length || 0})
            </button>
            <button
              className={`level-pill ${activeCategory === '5mark' ? 'active' : ''}`}
              onClick={() => setActiveCategory('5mark')}
              style={{ padding: '8px 20px', borderRadius: '20px' }}
            >
              5-Mark Explanatory Qs ({vivaData.five_mark_questions?.length || 0})
            </button>
            <button
              className={`level-pill ${activeCategory === 'viva' ? 'active' : ''}`}
              onClick={() => setActiveCategory('viva')}
              style={{ padding: '8px 20px', borderRadius: '20px' }}
            >
              🛡️ Examiner Defense Qs ({vivaData.viva_questions?.length || 0})
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {/* 2-Mark Questions */}
            {(activeCategory === 'all' || activeCategory === '2mark') && vivaData.two_mark_questions?.map((q, idx) => {
              const key = `2m_${idx}`;
              const isOpen = expandedIndex[key];
              return (
                <div
                  key={key}
                  className="glass-panel"
                  style={{
                    padding: '20px',
                    borderLeft: '4px solid #38bdf8',
                    background: isOpen ? 'rgba(56,189,248,0.03)' : 'rgba(15,23,42,0.6)',
                    transition: 'all 0.3s ease',
                    boxShadow: isOpen ? '0 4px 15px rgba(56,189,248,0.05)' : 'none'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                      <span className="badge" style={{ background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8', border: '1px solid rgba(56, 189, 248, 0.3)', marginTop: '2px', padding: '3px 8px' }}>
                        2 Marks
                      </span>
                      <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#f1f5f9', lineHeight: '1.4' }}>{q.question}</h4>
                    </div>
                    <button
                      className="btn-secondary"
                      style={{ fontSize: '0.75rem', padding: '6px 14px', borderRadius: '8px', flexShrink: 0 }}
                      onClick={() => toggleAnswer(key)}
                    >
                      {isOpen ? '🙈 Hide Answer' : '👁️ Show Model Answer'}
                    </button>
                  </div>

                  {isOpen && (
                    <div style={{ marginTop: '16px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '16px' }}>
                      {/* Answer Area */}
                      <div
                        className="md-output"
                        style={{
                          background: 'rgba(15,23,42,0.4)',
                          padding: '14px 18px',
                          borderRadius: '8px',
                          border: '1px solid rgba(56, 189, 248, 0.1)',
                          lineHeight: '1.6',
                          fontSize: '0.92rem',
                          color: '#e2e8f0',
                          marginBottom: '12px'
                        }}
                        dangerouslySetInnerHTML={renderMarkdown(q.answer)}
                      />

                      {/* Defense Strategy Tip */}
                      <div style={{
                        background: 'rgba(56, 189, 248, 0.08)',
                        border: '1px solid rgba(56, 189, 248, 0.15)',
                        padding: '10px 14px',
                        borderRadius: '8px',
                        fontSize: '0.8rem',
                        color: '#bae6fd',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        gap: '12px'
                      }}>
                        <div dangerouslySetInnerHTML={renderMarkdown(getDefenseTip('2mark'))} />
                        <button
                          type="button"
                          className="btn-secondary"
                          style={{ padding: '4px 10px', fontSize: '0.7rem', flexShrink: 0 }}
                          onClick={() => copyToClipboard(q.answer, key)}
                        >
                          {copiedKey === key ? '✅ Copied!' : '📋 Copy Solution'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}

            {/* 5-Mark Questions */}
            {(activeCategory === 'all' || activeCategory === '5mark') && vivaData.five_mark_questions?.map((q, idx) => {
              const key = `5m_${idx}`;
              const isOpen = expandedIndex[key];
              return (
                <div
                  key={key}
                  className="glass-panel"
                  style={{
                    padding: '20px',
                    borderLeft: '4px solid #6366f1',
                    background: isOpen ? 'rgba(99,102,241,0.03)' : 'rgba(15,23,42,0.6)',
                    transition: 'all 0.3s ease',
                    boxShadow: isOpen ? '0 4px 15px rgba(99,102,241,0.05)' : 'none'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                      <span className="badge" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)', marginTop: '2px', padding: '3px 8px' }}>
                        5 Marks
                      </span>
                      <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#f1f5f9', lineHeight: '1.4' }}>{q.question}</h4>
                    </div>
                    <button
                      className="btn-secondary"
                      style={{ fontSize: '0.75rem', padding: '6px 14px', borderRadius: '8px', flexShrink: 0 }}
                      onClick={() => toggleAnswer(key)}
                    >
                      {isOpen ? '🙈 Hide Answer' : '👁️ Show Model Answer'}
                    </button>
                  </div>

                  {isOpen && (
                    <div style={{ marginTop: '16px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '16px' }}>
                      {/* Answer Area */}
                      <div
                        className="md-output"
                        style={{
                          background: 'rgba(15,23,42,0.4)',
                          padding: '16px 20px',
                          borderRadius: '8px',
                          border: '1px solid rgba(99, 102, 241, 0.1)',
                          lineHeight: '1.65',
                          fontSize: '0.92rem',
                          color: '#e2e8f0',
                          marginBottom: '12px'
                        }}
                        dangerouslySetInnerHTML={renderMarkdown(q.answer)}
                      />

                      {/* Defense Strategy Tip */}
                      <div style={{
                        background: 'rgba(99, 102, 241, 0.08)',
                        border: '1px solid rgba(99, 102, 241, 0.15)',
                        padding: '10px 14px',
                        borderRadius: '8px',
                        fontSize: '0.8rem',
                        color: '#c7d2fe',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        gap: '12px'
                      }}>
                        <div dangerouslySetInnerHTML={renderMarkdown(getDefenseTip('5mark'))} />
                        <button
                          type="button"
                          className="btn-secondary"
                          style={{ padding: '4px 10px', fontSize: '0.7rem', flexShrink: 0 }}
                          onClick={() => copyToClipboard(q.answer, key)}
                        >
                          {copiedKey === key ? '✅ Copied!' : '📋 Copy Solution'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}

            {/* Viva Defense Questions */}
            {(activeCategory === 'all' || activeCategory === 'viva') && vivaData.viva_questions?.map((q, idx) => {
              const key = `viva_${idx}`;
              const isOpen = expandedIndex[key];
              return (
                <div
                  key={key}
                  className="glass-panel"
                  style={{
                    padding: '20px',
                    borderLeft: '4px solid var(--gold-main)',
                    background: isOpen ? 'rgba(212,175,55,0.03)' : 'rgba(15,23,42,0.6)',
                    transition: 'all 0.3s ease',
                    boxShadow: isOpen ? '0 4px 15px rgba(212,175,55,0.05)' : 'none'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                      <span className="badge" style={{ background: 'rgba(212, 175, 55, 0.15)', color: '#fbbf24', border: '1px solid var(--border-gold)', marginTop: '2px', padding: '3px 8px' }}>
                        🛡️ Viva Defense
                      </span>
                      <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#f1f5f9', lineHeight: '1.4' }}>{q.question}</h4>
                    </div>
                    <button
                      className="btn-secondary"
                      style={{ fontSize: '0.75rem', padding: '6px 14px', borderRadius: '8px', flexShrink: 0 }}
                      onClick={() => toggleAnswer(key)}
                    >
                      {isOpen ? '🙈 Hide Defense Answer' : '👁️ Show Defense Solution'}
                    </button>
                  </div>

                  {isOpen && (
                    <div style={{ marginTop: '16px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '16px' }}>
                      {/* Answer Area */}
                      <div
                        className="md-output"
                        style={{
                          background: 'rgba(15,23,42,0.4)',
                          padding: '18px 22px',
                          borderRadius: '8px',
                          border: '1px solid rgba(212, 175, 55, 0.15)',
                          lineHeight: '1.7',
                          fontSize: '0.92rem',
                          color: '#e2e8f0',
                          marginBottom: '12px'
                        }}
                        dangerouslySetInnerHTML={renderMarkdown(q.answer)}
                      />

                      {/* Defense Strategy Tip */}
                      <div style={{
                        background: 'rgba(212, 175, 55, 0.08)',
                        border: '1px solid rgba(212, 175, 55, 0.15)',
                        padding: '12px 16px',
                        borderRadius: '8px',
                        fontSize: '0.8rem',
                        color: '#fef08a',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        gap: '12px'
                      }}>
                        <div dangerouslySetInnerHTML={renderMarkdown(getDefenseTip('viva'))} />
                        <button
                          type="button"
                          className="btn-secondary"
                          style={{ padding: '4px 10px', fontSize: '0.7rem', flexShrink: 0 }}
                          onClick={() => copyToClipboard(q.answer, key)}
                        >
                          {copiedKey === key ? '✅ Copied!' : '📋 Copy Solution'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
