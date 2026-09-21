import React, { useRef, useState, useEffect } from 'react';
import { Play, Pause, Volume2, VolumeX, Maximize, RotateCcw, AlertCircle, Eye } from 'lucide-react';
import LanguageSelector from './LanguageSelector';
import AccessibilityControls from './AccessibilityControls';

export default function VideoPlayer({ lecture, metadata }) {
  const videoRef = useRef(null);
  const audioRef = useRef(null);
  const userPausedRef = useRef(false);

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

  // Global Keyboard Navigation Listener
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Don't intercept when focused inside text input or textarea
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;

      switch (e.key) {
        case ' ':
        case 'k':
        case 'K':
          e.preventDefault();
          togglePlay();
          break;
        case 'm':
        case 'M':
          e.preventDefault();
          toggleMute();
          break;
        case 'd':
        case 'D':
          e.preventDefault();
          setAdEnabled(prev => !prev);
          setAnnouncement(`Audio description ${!adEnabled ? 'enabled' : 'disabled'}`);
          break;
        case 'l':
        case 'L':
          e.preventDefault();
          setLanguage(prev => {
            const nextLang = prev === 'en' ? 'hi' : 'en';
            setAnnouncement(`Language switched to ${nextLang === 'en' ? 'English' : 'Hindi'}`);
            return nextLang;
          });
          break;
        case 'ArrowLeft':
          e.preventDefault();
          if (videoRef.current) {
            const newTime = Math.max(0, videoRef.current.currentTime - 5);
            performSeek(newTime);
          }
          break;
        case 'ArrowRight':
          e.preventDefault();
          if (videoRef.current) {
            const newTime = Math.min(duration, videoRef.current.currentTime + 5);
            performSeek(newTime);
          }
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isPlaying, isAdPlaying, adEnabled, language, duration, events]);

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

    // Pause lecture video
    videoRef.current.pause();
    setIsPlaying(false);
    setIsAdPlaying(true);
    setCurrentEvent(evt);
    userPausedRef.current = false;

    // Mark event as played
    setPlayedEventIds(prev => new Set(prev).add(evt.event_id));

    // Select audio & text based on language setting
    const audioSrc = language === 'hi' ? evt.audio_hi : evt.audio_en;
    const diagramType = evt.diagram_type || 'diagram';

    audioRef.current.src = audioSrc;
    // Screen reader announcement: concise status prompt to avoid double audio overlap with TTS MP3
    setAnnouncement(`Audio description playing: ${diagramType}`);

    // Play AD audio
    audioRef.current.play().catch(err => {
      console.error("Audio playback error:", err);
      resumeVideoPlayback();
    });
  };

  const handleAudioEnded = () => {
    resumeVideoPlayback();
  };

  const resumeVideoPlayback = () => {
    setIsAdPlaying(false);
    setCurrentEvent(null);
    if (!userPausedRef.current && videoRef.current) {
      videoRef.current.play();
      setIsPlaying(true);
      setAnnouncement("Audio description finished. Resuming video.");
    } else {
      setAnnouncement("Audio description finished. Video paused.");
    }
  };

  const togglePlay = () => {
    if (isAdPlaying) {
      // If user pauses while AD is playing, track manual pause intent
      if (audioRef.current && !audioRef.current.paused) {
        audioRef.current.pause();
        userPausedRef.current = true;
        setAnnouncement("Audio description paused.");
      } else if (audioRef.current && audioRef.current.paused) {
        audioRef.current.play();
        userPausedRef.current = false;
        setAnnouncement("Resuming audio description.");
      }
      return;
    }

    if (!videoRef.current) return;

    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
      userPausedRef.current = true;
    } else {
      videoRef.current.play();
      setIsPlaying(true);
      userPausedRef.current = false;
    }
  };

  const performSeek = (seekTime) => {
    if (videoRef.current) {
      videoRef.current.currentTime = seekTime;
      setCurrentTime(seekTime);

      // Replayability / Seek Invalidation:
      // Clear playedEventIds for all events at or after seekTime so re-watching triggers AD again
      setPlayedEventIds(prev => {
        const nextSet = new Set(prev);
        events.forEach(evt => {
          if (evt.timestamp >= seekTime - 0.5) {
            nextSet.delete(evt.event_id);
          }
        });
        return nextSet;
      });

      // Stop any active AD audio on seek
      if (isAdPlaying && audioRef.current) {
        audioRef.current.pause();
        setIsAdPlaying(false);
        setCurrentEvent(null);
      }
    }
  };

  const handleSeek = (e) => {
    const seekTime = parseFloat(e.target.value);
    performSeek(seekTime);
  };

  const toggleMute = () => {
    if (videoRef.current) {
      const nextMuted = !muted;
      videoRef.current.muted = nextMuted;
      if (audioRef.current) audioRef.current.muted = nextMuted;
      setMuted(nextMuted);
    }
  };

  return (
    <div className="card" style={{ padding: '1rem', background: '#000', borderRadius: '16px' }}>
      {/* Screen Reader Live Region for ARIA Announcements */}
      <div 
        role="status" 
        aria-live="polite" 
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
            background: 'rgba(15, 23, 42, 0.94)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            padding: '1.5rem',
            textAlign: 'center',
            zIndex: 10
          }}>
            <div style={{ background: 'var(--accent-primary)', color: '#fff', padding: '0.4rem 1rem', borderRadius: '20px', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Volume2 className="spin" size={16} /> Audio Description Playing ({language.toUpperCase()})
            </div>
            
            {/* Visual Callout Overlay for Low-Vision and Sighted Peers */}
            {(currentEvent.annotated_image_url || currentEvent.image_url) && (
              <div style={{ maxWidth: '65%', maxHeight: '45%', marginBottom: '0.75rem', borderRadius: '8px', overflow: 'hidden', border: '2px solid var(--accent-primary)' }}>
                <img
                  src={currentEvent.annotated_image_url || currentEvent.image_url}
                  alt={`Diagram region visual callout for event ${currentEvent.event_id}`}
                  style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                />
              </div>
            )}

            <p style={{ fontSize: '1.1rem', color: '#fff', maxWidth: '700px', lineHeight: 1.4, marginBottom: '0.75rem', fontStyle: 'italic' }}>
              "{language === 'hi' ? currentEvent.explanation_hi : currentEvent.explanation_en}"
            </p>

            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Lecture video automatically paused. Press Space or K to pause audio narrative.
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
              aria-label={isPlaying || isAdPlaying ? "Pause" : "Play"}
            >
              {isPlaying || isAdPlaying ? <Pause size={20} /> : <Play size={20} />}
              <span>{isPlaying || isAdPlaying ? 'Pause' : 'Play'}</span>
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

