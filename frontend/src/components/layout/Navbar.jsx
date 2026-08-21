import React from 'react';
import { Eye, BookOpen, Volume2, Moon, Sun } from 'lucide-react';

export default function Navbar({ currentView, setView, isHighContrast, toggleHighContrast }) {
  return (
    <header style={{ borderBottom: '1px solid var(--border-color)', background: 'var(--bg-card)', padding: '1rem 0' }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div 
          onClick={() => setView('landing')}
          style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', cursor: 'pointer' }}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && setView('landing')}
          aria-label="EduVision Home"
        >
          <div style={{ background: 'var(--accent-primary)', padding: '0.5rem', borderRadius: '8px', display: 'flex' }}>
            <Eye size={24} color="#fff" />
          </div>
          <div>
            <h1 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)', margin: 0 }}>EduVision</h1>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0 }}>Accessible Diagram-to-Speech Platform</p>
          </div>
        </div>

        <nav aria-label="Main Navigation">
          <ul style={{ display: 'flex', listStyle: 'none', gap: '1rem', alignItems: 'center' }}>
            <li>
              <button
                onClick={() => setView('landing')}
                className={`btn ${currentView === 'landing' ? 'btn-primary' : 'btn-secondary'}`}
                aria-current={currentView === 'landing' ? 'page' : undefined}
              >
                Home
              </button>
            </li>
            <li>
              <button
                onClick={() => setView('catalog')}
                className={`btn ${currentView === 'catalog' || currentView === 'player' ? 'btn-primary' : 'btn-secondary'}`}
                aria-current={currentView === 'catalog' ? 'page' : undefined}
              >
                <BookOpen size={18} /> Catalog
              </button>
            </li>
            <li>
              <button
                onClick={toggleHighContrast}
                className="btn btn-secondary"
                aria-label={isHighContrast ? "Disable High Contrast Mode" : "Enable High Contrast Mode"}
                title="Toggle High Contrast Mode"
              >
                {isHighContrast ? <Sun size={18} /> : <Moon size={18} />}
                <span>{isHighContrast ? 'Normal' : 'High Contrast'}</span>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
