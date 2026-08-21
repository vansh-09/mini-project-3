import React from 'react';
import { Globe } from 'lucide-react';

export default function LanguageSelector({ currentLanguage, onChangeLanguage }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <Globe size={18} style={{ color: 'var(--text-muted)' }} />
      <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Audio Description Language:</span>
      <div style={{ display: 'inline-flex', borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--border-color)' }}>
        <button
          onClick={() => onChangeLanguage('en')}
          style={{
            padding: '0.4rem 0.8rem',
            border: 'none',
            background: currentLanguage === 'en' ? 'var(--accent-primary)' : 'var(--bg-card-hover)',
            color: '#fff',
            fontWeight: 600,
            cursor: 'pointer',
            fontSize: '0.85rem'
          }}
          aria-label="Select English Audio Descriptions"
        >
          English
        </button>
        <button
          onClick={() => onChangeLanguage('hi')}
          style={{
            padding: '0.4rem 0.8rem',
            border: 'none',
            background: currentLanguage === 'hi' ? 'var(--accent-primary)' : 'var(--bg-card-hover)',
            color: '#fff',
            fontWeight: 600,
            cursor: 'pointer',
            fontSize: '0.85rem'
          }}
          aria-label="Select Hindi Audio Descriptions (हिंदी)"
        >
          हिंदी (Hindi)
        </button>
      </div>
    </div>
  );
}
