import React from 'react';
import { Play, Volume2, Tag, Clock } from 'lucide-react';

export default function LectureCard({ lecture, onSelect }) {
  const getSubjectBadge = (subject) => {
    switch (subject?.toLowerCase()) {
      case 'physics': return { bg: '#3b82f6', text: '#fff' };
      case 'biology': return { bg: '#10b981', text: '#fff' };
      case 'chemistry': return { bg: '#ec4899', text: '#fff' };
      default: return { bg: 'var(--accent-primary)', text: '#fff' };
    }
  };

  const badge = getSubjectBadge(lecture.subject);

  return (
    <article className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
          <span style={{ 
            backgroundColor: badge.bg, 
            color: badge.text, 
            padding: '0.25rem 0.75rem', 
            borderRadius: '20px', 
            fontSize: '0.8rem', 
            fontWeight: 700 
          }}>
            {lecture.subject || 'General Science'}
          </span>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
            <Volume2 size={14} /> {lecture.events_count || 0} Audio Descriptions
          </span>
        </div>

        <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>
          {lecture.title}
        </h3>

        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.5rem', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
          {lecture.description || 'Interactive lecture video with automated diagram vision analysis and bilingual audio description.'}
        </p>
      </div>

      <button
        onClick={() => onSelect(lecture)}
        className="btn btn-primary"
        style={{ width: '100%', justifyContent: 'center' }}
        aria-label={`Play lecture: ${lecture.title}`}
      >
        <Play size={18} /> Play Lecture & Audio Descriptions
      </button>
    </article>
  );
}
