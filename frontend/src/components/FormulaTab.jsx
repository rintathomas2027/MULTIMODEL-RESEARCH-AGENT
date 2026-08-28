import React, { useState } from 'react';
import { api } from '../api';

export default function FormulaTab({ document }) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleSynthesize = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    try {
      const data = await api.getFormulaCode(document.id, query);
      setResult(data);
    } catch (err) {
      alert(`Formula to Code synthesis failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const copyCode = (codeText) => {
    navigator.clipboard.writeText(codeText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Search / Input Control Bar */}
      <div className="glass-panel" style={{ padding: '20px 24px' }}>
        <form onSubmit={handleSynthesize} style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <input
            type="text"
            className="glass-input"
            style={{ flex: 1, padding: '12px 16px', fontSize: '0.9rem' }}
            placeholder="Target equation / formula (e.g. Attention mechanism, Loss function, Cosine similarity)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
            style={{
              padding: '12px 24px',
              fontSize: '0.9rem',
              whiteSpace: 'nowrap',
              minWidth: '150px'
            }}
          >
            {loading ? 'Synthesizing...' : '⚡ Synthesize Code'}
          </button>
        </form>
      </div>

      {/* Loading state indicator matching the UI screenshot */}
      {loading && (
        <div className="glass-panel" style={{
          padding: '60px 20px',
          textAlign: 'center',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '16px'
        }}>
          <div style={{
            width: '54px',
            height: '54px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, rgba(212,175,55,0.2), rgba(184,134,11,0.4))',
            border: '1px solid var(--border-gold)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.8rem'
          }}>
            🧮
          </div>
          <div style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc' }}>
            Compiling Mathematical Notation into PyTorch/Python...
          </div>
          <p style={{ fontSize: '0.82rem', color: '#94a3b8', maxWidth: '480px' }}>
            Extracting mathematical operators, dimensional shapes, and algorithmic logic from "{document.title}"
          </p>
        </div>
      )}

      {/* Empty / Initial State (when not loading and no result yet) */}
      {!loading && !result && (
        <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: '#94a3b8' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '12px' }}>🧮</div>
          <h3 style={{ fontSize: '1.1rem', color: '#f8fafc', fontWeight: 700, marginBottom: '6px' }}>
            Multimodal Math & Algorithm Synthesizer
          </h3>
          <p style={{ fontSize: '0.85rem', maxWidth: '540px', margin: '0 auto' }}>
            Specify a target formula/loss function above or click synthesize to automatically extract the main algorithm from <strong>{document.title}</strong> into clean, production-ready PyTorch/NumPy code.
          </p>
        </div>
      )}

      {/* Synthesized Formula & Code Output */}
      {!loading && result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Header & LaTeX Math Card */}
          <div className="glass-panel" style={{ padding: '24px', borderLeft: '4px solid var(--gold-main)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
              <div>
                <span className="badge badge-gold" style={{ marginBottom: '6px', display: 'inline-block' }}>
                  Mathematical Formulation
                </span>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f8fafc' }}>
                  {result.formula_name || 'Extracted Formula'}
                </h3>
              </div>
              {result.complexity_analysis && (
                <div style={{
                  background: 'rgba(212, 175, 55, 0.1)',
                  border: '1px solid var(--border-gold)',
                  borderRadius: '8px',
                  padding: '6px 14px',
                  fontSize: '0.8rem',
                  color: '#fbbf24',
                  fontWeight: 600
                }}>
                  ⚡ {result.complexity_analysis}
                </div>
              )}
            </div>

            {/* LaTeX Mathematical Notation */}
            {result.latex_notation && (
              <div style={{
                background: 'rgba(18, 19, 22, 0.7)',
                border: '1px solid rgba(212, 175, 55, 0.25)',
                borderRadius: '10px',
                padding: '20px',
                margin: '12px 0 16px 0',
                textAlign: 'center',
                overflowX: 'auto'
              }}>
                <div style={{ fontSize: '1.15rem', color: '#f8fafc', fontFamily: 'serif', letterSpacing: '0.5px' }}>
                  {result.latex_notation}
                </div>
              </div>
            )}

            {/* Mathematical Explanation */}
            {result.mathematical_explanation && (
              <div style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: '1.6', marginTop: '12px' }}>
                <strong style={{ color: '#f8fafc' }}>Explanation: </strong>
                {result.mathematical_explanation}
              </div>
            )}
          </div>

          {/* Variable Definitions */}
          {result.variable_definitions && result.variable_definitions.length > 0 && (
            <div className="glass-panel" style={{ padding: '20px 24px' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f8fafc', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                📌 Variable & Symbol Breakdown
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '10px' }}>
                {result.variable_definitions.map((item, idx) => (
                  <div key={idx} style={{
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '8px',
                    padding: '10px 14px',
                    display: 'flex',
                    alignItems: 'baseline',
                    gap: '10px'
                  }}>
                    <code style={{
                      color: '#fbbf24',
                      background: 'rgba(212, 175, 55, 0.15)',
                      padding: '2px 8px',
                      borderRadius: '4px',
                      fontWeight: 700,
                      fontSize: '0.88rem'
                    }}>
                      {item.symbol}
                    </code>
                    <span style={{ fontSize: '0.83rem', color: '#94a3b8' }}>
                      {item.description}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Executable Code Block */}
          {result.python_code && (
            <div className="glass-panel" style={{ padding: '0', overflow: 'hidden' }}>
              <div style={{
                background: '#121316',
                padding: '12px 20px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                borderBottom: '1px solid rgba(255, 255, 255, 0.08)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ef4444', display: 'inline-block' }}></span>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#f59e0b', display: 'inline-block' }}></span>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10b981', display: 'inline-block' }}></span>
                  <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#94a3b8', marginLeft: '8px', fontFamily: 'var(--font-code)' }}>
                    pytorch_implementation.py
                  </span>
                </div>

                <button
                  onClick={() => copyCode(result.python_code)}
                  className="btn-secondary"
                  style={{
                    padding: '4px 12px',
                    fontSize: '0.78rem',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    background: copied ? '#10b981' : 'rgba(255, 255, 255, 0.1)',
                    color: '#ffffff',
                    border: 'none',
                    transition: 'all 0.2s ease'
                  }}
                >
                  {copied ? '✓ Copied!' : '📋 Copy Code'}
                </button>
              </div>

              <pre style={{
                margin: 0,
                padding: '20px',
                background: '#0a0a0c',
                color: '#e2e8f0',
                fontFamily: 'var(--font-code)',
                fontSize: '0.88rem',
                lineHeight: '1.6',
                overflowX: 'auto'
              }}>
                <code>{result.python_code}</code>
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
