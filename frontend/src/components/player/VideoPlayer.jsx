import React, { useRef, useState, useEffect } from 'react';
import { Play, Pause, Volume2, VolumeX, Maximize, RotateCcw, AlertCircle } from 'lucide-react';
import LanguageSelector from './LanguageSelector';
import AccessibilityControls from './AccessibilityControls';

export default function VideoPlayer({ lecture, metadata }) {
  const videoRef = useRef(null);
  const audioRef = useRef(null);

  const [isPlaying, setIsPlaying] = useState(false);
  const [isAdPlaying, setIsAdPlaying] = useState(false);
  const [adEnabled, setAdEnabled] = useState(true);
  const [language, setLanguage] = useState('en'); // 'en' | 'hi'
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [muted, setMuted] = useState(false);
  const [currentEvent, setCurrentEvent] = useState(null);
  const [playedEventIds, setPlayedEventIds] = useState(new Set());
  const [announcement, setAnnouncement] = useState('');

  const events = metadata?.events || [];

  // Handle Video Time Update & Diagram Event Audio Triggers
  const handleTimeUpdate = () => {
    if (!videoRef.current || isAdPlaying || !adEnabled) return;

    const time = videoRef.current.currentTime;
    setCurrentTime(time);

    // Check if timestamp crosses an unplayed event timestamp
    for (const evt of events) {
      if (!playedEventIds.has(evt.event_id) && Math.abs(time - evt.timestamp) <= 1.5) {
        triggerAudioDescription(evt);
        break;
      }
    }
  };

  const triggerAudioDescription = (evt) => {
    if (!videoRef.current || !audioRef.current) return;

    // 1. Pause video
    videoRef.current.pause();
    setIsPlaying(false);
    setIsAdPlaying(true);
    setCurrentEvent(evt);

    // Mark event as played
    setPlayedEventIds(prev => new Set(prev).add(evt.event_id));

    // Choose language audio file
    const audioSrc = language === 'hi' ? evt.audio_hi : evt.audio_en;
    const explanationText = language === 'hi' ? evt.explanation_hi : evt.explanation_en;

    audioRef.current.src = audioSrc;
    setAnnouncement(`Diagram Audio Description: ${explanationText}`);

    // 2. Play AD audio
    audioRef.current.play().catch(err => {
      console.error("Audio playback error:", err);
      // Fallback resume if audio fails
      resumeVideoPlayback();
    });
  };

  const handleAudioEnded = () => {
    resumeVideoPlayback();
  };

  const resumeVideoPlayback = () => {
    setIsAdPlaying(false);
    setCurrentEvent(null);
    if (videoRef.current) {
      videoRef.current.play();
      setIsPlaying(true);
      setAnnouncement("Audio Description complete. Resuming lecture video.");
    }
  };

  const togglePlay = () => {
    if (isAdPlaying) return; // Prevent breaking AD audio
    if (!videoRef.current) return;

    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const handleSeek = (e) => {
    const seekTime = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.currentTime = seekTime;
      setCurrentTime(seekTime);
    }
  };

  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !muted;
      setMuted(!muted);
    }
  };

  return (
    <div className="card" style={{ padding: '1rem', background: '#000', borderRadius: '16px' }}>
      {/* Screen Reader Live Region for ARIA Announcements */}
      <div 
        role="status" 
        aria-live="assertive" 
        style={{ position: 'absolute', width: '1px', height: '1px', overflow: 'hidden', clip: 'rect(0,0,0,0)' }}
      >
        {announcement}
      </div>

      {/* Video Container */}
      <div style={{ position: 'relative', width: '100%', aspectRatio: '16/9', background: '#0f172a', borderRadius: '12px', overflow: 'hidden' }}>
        <video
          ref={videoRef}
          src={lecture.video_url || "/storage/uploads/sample.mp4"}
          style={{ width: '100%', height: '100%', objectFit: 'contain' }}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={() => setDuration(videoRef.current?.duration || 0)}
          onEnded={() => setIsPlaying(false)}
          onClick={togglePlay}
          aria-label={lecture.title}
        />

        {/* Hidden HTML5 Audio Element for AD Playback */}
        <audio ref={audioRef} onEnded={handleAudioEnded} />

        {/* Overlay when Diagram AD is Active */}
        {isAdPlaying && currentEvent && (
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'rgba(15, 23, 42, 0.92)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            padding: '2rem',
            textAlign: 'center',
            zIndex: 10
          }}>
            <div style={{ background: 'var(--accent-primary)', color: '#fff', padding: '0.4rem 1rem', borderRadius: '20px', fontSize: '0.85rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Volume2 className="spin" size={16} /> Audio Description Playing ({language.toUpperCase()})
            </div>
            
            <p style={{ fontSize: '1.2rem', color: '#fff', maxWidth: '700px', lineHeight: 1.5, marginBottom: '1rem', fontStyle: 'italic' }}>
              "{language === 'hi' ? currentEvent.explanation_hi : currentEvent.explanation_en}"
            </p>

            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Lecture video automatically paused. Will resume when narrative ends.
            </span>
          </div>
        )}
      </div>

      {/* Interactive Player Controls */}
      <div style={{ padding: '1rem 0.5rem 0.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {/* Progress bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {Math.floor(currentTime / 60)}:{('0' + Math.floor(currentTime % 60)).slice(-2)}
          </span>
          <input
            type="range"
            min="0"
            max={duration || 100}
            value={currentTime}
            onChange={handleSeek}
            style={{ flex: 1, accentColor: 'var(--accent-primary)', cursor: 'pointer' }}
            aria-label="Seek video position"
          />
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {Math.floor(duration / 60)}:{('0' + Math.floor(duration % 60)).slice(-2)}
          </span>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <button 
              onClick={togglePlay} 
              className="btn btn-primary"
              aria-label={isPlaying ? "Pause video" : "Play video"}
            >
              {isPlaying ? <Pause size={20} /> : <Play size={20} />}
              <span>{isPlaying ? 'Pause' : 'Play'}</span>
            </button>

            <button onClick={toggleMute} className="btn btn-secondary" aria-label={muted ? "Unmute" : "Mute"}>
              {muted ? <VolumeX size={18} /> : <Volume2 size={18} />}
            </button>

            <AccessibilityControls
              adEnabled={adEnabled}
              setAdEnabled={setAdEnabled}
            />
          </div>

          <LanguageSelector
            currentLanguage={language}
            onChangeLanguage={setLanguage}
          />
        </div>
      </div>
    </div>
  );
}
