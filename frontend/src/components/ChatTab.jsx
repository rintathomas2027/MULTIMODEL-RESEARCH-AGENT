import React, { useState, useEffect, useRef } from 'react';
import { api } from '../api';

export default function ChatTab({ document }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Dual summary states
  const [summary, setSummary] = useState(document.summary || '');
  const [summaryShort, setSummaryShort] = useState(document.summary_short || '');
  const [summaryMode, setSummaryMode] = useState('detailed'); // 'detailed' | 'short'
  const [loadingSummary, setLoadingSummary] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (document) {
      loadHistory();
      setSummary(document.summary || '');
      setSummaryShort(document.summary_short || '');
    }
  }, [document]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadHistory = async () => {
    try {
      const history = await api.getChatHistory(document.id);
      const formatted = [];
      history.forEach(item => {
        formatted.push({ role: 'user', text: item.question });
        formatted.push({ role: 'assistant', text: item.answer });
      });
      setMessages(formatted);
    } catch (err) {
      console.error('Failed to load chat history:', err);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userText }]);
    setLoading(true);

    try {
      const res = await api.sendChatMessage(document.id, userText);
      setMessages(prev => [...prev, { role: 'assistant', text: res.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: `⚠️ Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSummarize = async (mode) => {
    setLoadingSummary(true);
    try {
      const res = await api.summarizeDocument(document.id, mode);
      setSummary(res.summary || '');
      setSummaryShort(res.summary_short || '');
    } catch (err) {
      alert(`Failed to generate summary: ${err.message}`);
    } finally {
      setLoadingSummary(false);
    }
  };

  const renderMarkdown = (text) => {
    if (window.marked) {
      return { __html: window.marked.parse(text) };
    }
    return { __html: text.replace(/\n/g, '<br/>') };
  };

  const activeSummary = summaryMode === 'detailed' ? summary : summaryShort;
  const hasActiveSummary = !!activeSummary;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Paper Summary Bar */}
      <div className="glass-panel" style={{ padding: '20px 24px', borderLeft: '4px solid var(--gold-main)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '1.3rem' }}>📄</span>
            <div>
              <span style={{ fontWeight: 800, fontSize: '1.05rem', color: '#f8fafc' }}>AI Document Summarizer</span>
              <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>
                Select summary detail levels mapped directly to textbook sections
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            {/* Mode Segmented Controls */}
            <div style={{
              display: 'flex',
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid var(--border-gold)',
              borderRadius: '20px',
              padding: '2px'
            }}>
              <button
                type="button"
                onClick={() => setSummaryMode('detailed')}
                style={{
                  padding: '6px 14px',
                  borderRadius: '18px',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  border: 'none',
                  background: summaryMode === 'detailed' ? 'var(--gold-main)' : 'transparent',
                  color: summaryMode === 'detailed' ? 'white' : '#94a3b8',
                  transition: 'all 0.2s ease'
                }}
              >
                📑 Detailed Summary
              </button>
              <button
                type="button"
                onClick={() => setSummaryMode('short')}
                style={{
                  padding: '6px 14px',
                  borderRadius: '18px',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  border: 'none',
                  background: summaryMode === 'short' ? 'var(--gold-main)' : 'transparent',
                  color: summaryMode === 'short' ? 'white' : '#94a3b8',
                  transition: 'all 0.2s ease'
                }}
              >
                📝 Short Abstract
              </button>
            </div>

            {hasActiveSummary && (
              <button
                className="btn-secondary"
                style={{ fontSize: '0.75rem', padding: '6px 12px' }}
                onClick={() => handleSummarize(summaryMode)}
                disabled={loadingSummary}
              >
                {loadingSummary ? '⏳ Summarizing...' : '🔄 Re-Generate'}
              </button>
            )}
          </div>
        </div>

        {/* Display active summary contents */}
        {hasActiveSummary ? (
          <div
            className="md-output-premium"
            style={{
              padding: '24px',
              borderRadius: '10px',
              background: 'rgba(15, 23, 42, 0.45)',
              border: '1px solid rgba(212, 175, 55, 0.15)',
              maxHeight: '400px',
              overflowY: 'auto',
              boxShadow: 'inset 0 2px 8px rgba(0, 0, 0, 0.2)',
              color: '#e2e8f0'
            }}
          >
            <style>{`
              .md-output-premium p {
                margin-bottom: 1.25rem;
                font-size: 1.05rem;
                line-height: 1.8;
                color: inherit;
              }
              .md-output-premium h1, .md-output-premium h2, .md-output-premium h3 {
                margin-top: 1.5rem;
                margin-bottom: 0.8rem;
                font-weight: 800;
                color: inherit;
              }
              .md-output-premium ul, .md-output-premium ol {
                margin-bottom: 1.25rem;
                padding-left: 1.5rem;
                list-style-type: disc;
              }
              .md-output-premium li {
                margin-bottom: 0.5rem;
                font-size: 1.05rem;
                line-height: 1.8;
                color: inherit;
              }
            `}</style>
            <div dangerouslySetInnerHTML={renderMarkdown(activeSummary)} />
          </div>
        ) : (
          <div style={{
            padding: '24px',
            textAlign: 'center',
            background: 'rgba(255, 255, 255, 0.01)',
            borderRadius: '10px',
            border: '1px dashed var(--border-gold)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '12px'
          }}>
            <div style={{ fontSize: '1.8rem' }}>🧠</div>
            <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
              No {summaryMode === 'detailed' ? 'Detailed Summary' : 'Short Abstract'} has been generated for this paper yet.
            </p>
            <button
              className="btn-primary"
              style={{ fontSize: '0.8rem', padding: '8px 18px' }}
              onClick={() => handleSummarize(summaryMode)}
              disabled={loadingSummary}
            >
              {loadingSummary ? '⏳ Generating Summary...' : `⚡ Generate ${summaryMode === 'detailed' ? 'Detailed Summary' : 'Short Abstract'}`}
            </button>
          </div>
        )}
      </div>

      {/* RAG Chat Box */}
      <div className="glass-panel chat-container" style={{ borderTop: '1px solid var(--border-gold)' }}>
        <div style={{ padding: '14px 20px', borderBottom: '1px solid var(--border-glass)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontWeight: 700, fontSize: '0.95rem' }}>💬 Document-Grounded Q&A (ChromaDB Vector RAG)</span>
          <span className="badge" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
            Gemini 1.5 Flash
          </span>
        </div>

        <div className="chat-messages" style={{ height: '350px' }}>
          {messages.length === 0 ? (
            <div style={{ textOverflow: 'ellipsis', margin: 'auto', textAlign: 'center', color: '#94a3b8', padding: '20px' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>💡</div>
              <p style={{ fontWeight: 600, color: '#e2e8f0', marginBottom: '4px' }}>Ask anything about "{document.title}"</p>
              <p style={{ fontSize: '0.8rem' }}>Ask about methodology, algorithms, dataset, results, or mathematical proofs.</p>
            </div>
          ) : (
            messages.map((m, idx) => (
              <div key={idx} className={`message-bubble ${m.role}`} style={{
                borderRadius: '12px',
                padding: '12px 16px',
                border: m.role === 'assistant' ? '1px solid var(--border-gold)' : 'none',
                maxWidth: '85%'
              }}>
                <div style={{ fontSize: '0.72rem', opacity: 0.8, marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.05em', color: m.role === 'user' ? '#94a3b8' : 'var(--gold-main)', fontWeight: 700 }}>
                  {m.role === 'user' ? '👤 You' : '⚡ ScholarPulse AI'}
                </div>
                <div className="md-output" dangerouslySetInnerHTML={renderMarkdown(m.text)} />
              </div>
            ))
          )}
          {loading && (
            <div className="message-bubble assistant" style={{ border: '1px solid var(--border-gold)' }}>
              <span style={{ color: '#94a3b8' }}>🧠 ScholarPulse AI is analyzing document context...</span>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <form onSubmit={handleSend} style={{ padding: '16px', borderTop: '1px solid var(--border-glass)', display: 'flex', gap: '10px' }}>
          <input
            type="text"
            className="glass-input"
            style={{ flex: 1, borderRadius: '20px', padding: '10px 18px' }}
            placeholder={`Ask a question about ${document.title}...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button className="btn-primary" type="submit" disabled={loading || !input.trim()} style={{ borderRadius: '20px', padding: '10px 22px' }}>
            Send 🚀
          </button>
        </form>
      </div>
    </div>
  );
}
