import React from 'react';

export default function Footer() {
  return (
    <footer style={{ borderTop: '1px solid var(--border-color)', padding: '2rem 0', marginTop: '4rem', background: 'var(--bg-card)' }}>
      <div className="container" style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        <p>EduVision — Diagram to Speech Pipeline & Accessible Web UI</p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.8rem' }}>
          Designed for visually impaired students. Fully compliant with WCAG 2.1 accessibility standards.
        </p>
      </div>
    </footer>
  );
}
