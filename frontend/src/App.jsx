import React, { useState } from 'react';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Landing from './pages/Landing';
import Catalog from './pages/Catalog';
import LecturePlayer from './pages/LecturePlayer';

export default function App() {
  const [currentView, setView] = useState('landing'); // 'landing' | 'catalog' | 'player'
  const [selectedLectureId, setSelectedLectureId] = useState(null);
  const [isHighContrast, setIsHighContrast] = useState(false);

  const toggleHighContrast = () => {
    setIsHighContrast(!isHighContrast);
    if (!isHighContrast) {
      document.body.classList.add('high-contrast');
    } else {
      document.body.classList.remove('high-contrast');
    }
  };

  const handleSelectLecture = (lecture) => {
    setSelectedLectureId(lecture.lecture_id);
    setView('player');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <a href="#main-content" className="skip-link">Skip to main content</a>

      <Navbar
        currentView={currentView}
        setView={setView}
        isHighContrast={isHighContrast}
        toggleHighContrast={toggleHighContrast}
      />

      <div id="main-content" style={{ flex: 1 }}>
        {currentView === 'landing' && <Landing setView={setView} />}
        {currentView === 'catalog' && <Catalog onSelectLecture={handleSelectLecture} />}
        {currentView === 'player' && (
          <LecturePlayer
            lectureId={selectedLectureId}
            onBack={() => setView('catalog')}
          />
        )}
      </div>

      <Footer />
    </div>
  );
}
