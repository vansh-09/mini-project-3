import React from 'react';
import { Eye, BookOpen, Volume2, ShieldCheck, ArrowRight, Sparkles } from 'lucide-react';

export default function Landing({ setView }) {
  return (
    <main className="container" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
      {/* Hero Section */}
      <section style={{ textAlign: 'center', maxWidth: '850px', margin: '0 auto 4rem' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          background: 'rgba(99, 102, 241, 0.15)',
          color: 'var(--accent-primary)',
          padding: '0.4rem 1rem',
          borderRadius: '20px',
          fontSize: '0.85rem',
          fontWeight: 700,
          marginBottom: '1.5rem',
          border: '1px solid rgba(99, 102, 241, 0.3)'
        }}>
          <Sparkles size={16} /> AI Vision + Bilingual Audio Descriptions for STEM Education
        </div>

        <h1 style={{ fontSize: '3rem', fontWeight: 800, lineHeight: 1.2, marginBottom: '1.5rem', letterSpacing: '-0.02em' }}>
          Bridging STEM Accessibility for <span style={{ color: 'var(--accent-primary)' }}>Visually Impaired Students</span>
        </h1>

        <p style={{ fontSize: '1.2rem', color: 'var(--text-muted)', marginBottom: '2rem', lineHeight: 1.6 }}>
          EduVision automatically converts visual STEM diagrams—graphs, flowcharts, biological schematics, and chemical structures—into clear, pedagogical spoken explanations in English and Hindi.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <button onClick={() => setView('catalog')} className="btn btn-primary" style={{ padding: '0.9rem 2rem', fontSize: '1.05rem' }}>
            Explore Lecture Catalog <ArrowRight size={20} />
          </button>
        </div>
      </section>

      {/* Problem Statement & Solution */}
      <section className="grid" style={{ marginBottom: '4rem' }}>
        <div className="card">
          <div style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#ef4444', width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
            <Eye size={24} />
          </div>
          <h3 style={{ fontSize: '1.3rem', marginBottom: '0.5rem' }}>The Visual Accessibility Gap</h3>
          <p style={{ color: 'var(--text-muted)' }}>
            STEM lectures rely heavily on charts, graphs, equations, and diagrams. Standard screen readers read plain text but skip or give meaningless alt-text for complex visual figures.
          </p>
        </div>

        <div className="card">
          <div style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#10b981', width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
            <Volume2 size={24} />
          </div>
          <h3 style={{ fontSize: '1.3rem', marginBottom: '0.5rem' }}>Automated Audio Descriptions</h3>
          <p style={{ color: 'var(--text-muted)' }}>
            Our 3-step AI pipeline extracts video frames, runs computer vision detection + Groq VLM diagram understanding, and synthesizes bilingual spoken narration.
          </p>
        </div>

        <div className="card">
          <div style={{ background: 'rgba(6, 182, 212, 0.15)', color: '#06b6d4', width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
            <ShieldCheck size={24} />
          </div>
          <h3 style={{ fontSize: '1.3rem', marginBottom: '0.5rem' }}>Intelligent Non-Overlapping Player</h3>
          <p style={{ color: 'var(--text-muted)' }}>
            The Web player automatically pauses lecture playback when a diagram appears, plays the educational audio description, and resumes the video seamlessly.
          </p>
        </div>
      </section>

      {/* How It Works */}
      <section className="card" style={{ padding: '2.5rem', background: 'var(--bg-card)' }}>
        <h2 style={{ textAlign: 'center', fontSize: '1.8rem', marginBottom: '2rem' }}>How EduVision Works</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem', textAlign: 'center' }}>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--accent-primary)', marginBottom: '0.5rem' }}>01</div>
            <h4 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Frame & Timestamp Extraction</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>OpenCV extracts lecture video frames mapped precisely to timestamps (Contract 1).</p>
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--accent-secondary)', marginBottom: '0.5rem' }}>02</div>
            <h4 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Vision & OCR Analysis</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Grouped diagram events pass through OCR and Groq VLM vision models (Contract 2).</p>
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--accent-success)', marginBottom: '0.5rem' }}>03</div>
            <h4 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Educational GenAI & TTS</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>LLMs create 3-5 sentence narratives synthesized into English and Hindi MP3 files (Contract 3).</p>
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--accent-warning)', marginBottom: '0.5rem' }}>04</div>
            <h4 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Accessible Web Playback</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Students interact with the accessible player featuring pause → play AD → resume logic.</p>
          </div>
        </div>
      </section>
    </main>
  );
}
