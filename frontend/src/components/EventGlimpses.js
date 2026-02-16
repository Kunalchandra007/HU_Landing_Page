import React, { useState, useEffect } from 'react';
import { getCompletedEvents } from '../services/api';
import './EventGlimpses.css';

function EventGlimpses() {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [glimpses, setGlimpses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCompletedEvents = async () => {
      try {
        const completedEvents = await getCompletedEvents();
        
        // Add Alumni Meet as a static card at the beginning
        const alumniMeet = {
          id: 'alumni-meet',
          title: "Alumni Meet",
          description: "A heartwarming reunion of HU family members sharing memories and celebrating success stories",
          image_path: "images/logo.jpeg",
          video_url: "https://www.youtube.com/embed/tCmR4YyQGQE"
        };
        
        // Combine alumni meet with completed events
        setGlimpses([alumniMeet, ...completedEvents]);
      } catch (error) {
        console.error('Error fetching completed events:', error);
        // If API fails, still show Alumni Meet
        const alumniMeet = {
          id: 'alumni-meet',
          title: "Alumni Meet",
          description: "A heartwarming reunion of HU family members sharing memories and celebrating success stories",
          image_path: "images/logo.jpeg",
          video_url: "https://www.youtube.com/embed/tCmR4YyQGQE"
        };
        setGlimpses([alumniMeet]);
      } finally {
        setLoading(false);
      }
    };

    fetchCompletedEvents();
  }, []);

  const openVideo = (videoUrl) => {
    // Add autoplay parameter to the video URL
    const autoplayUrl = videoUrl.includes('?') 
      ? `${videoUrl}&autoplay=1` 
      : `${videoUrl}?autoplay=1`;
    setSelectedVideo(autoplayUrl);
  };

  const closeVideo = () => {
    setSelectedVideo(null);
  };

  if (loading) {
    return (
      <section className="event-glimpses">
        <div className="glimpses-container">
          <p>Loading event glimpses...</p>
        </div>
      </section>
    );
  }

  if (glimpses.length === 0) {
    return null; // Don't show section if no events
  }

  return (
    <section className="event-glimpses">
      <div className="glimpses-container">
        <div className="glimpses-header">
          <h2 className="glimpses-title">
            <span className="title-icon">🎉</span>
            Enjoy the Events with HU Family
          </h2>
          <p className="glimpses-subtitle">Relive the memorable moments from our past events</p>
        </div>

        <div className="glimpses-grid">
          {glimpses.map((glimpse) => (
            <div 
              key={glimpse.id} 
              className="glimpse-card"
              onClick={() => glimpse.video_url && openVideo(glimpse.video_url)}
            >
              <div className="glimpse-image-wrapper">
                {glimpse.video_url ? (
                  <>
                    <iframe
                      src={`${glimpse.video_url}?autoplay=1&mute=1&loop=1&playlist=${glimpse.video_url.split('/').pop()}&controls=0&modestbranding=1&rel=0`}
                      title={glimpse.title}
                      frameBorder="0"
                      allow="autoplay; muted"
                      className="glimpse-video-bg"
                    />
                    <div className="video-overlay"></div>
                  </>
                ) : (
                  <img src={`/${glimpse.image_path}`} alt={glimpse.title} />
                )}
                {glimpse.video_url && (
                  <div className="play-overlay">
                    <div className="play-button">
                      <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                        <circle cx="30" cy="30" r="30" fill="rgba(255, 255, 255, 0.9)" />
                        <path d="M24 18L42 30L24 42V18Z" fill="#ef4444" />
                      </svg>
                    </div>
                  </div>
                )}
              </div>
              <div className="glimpse-content">
                <h3 className="glimpse-title">{glimpse.title}</h3>
                <p className="glimpse-caption">{glimpse.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Video Modal */}
      {selectedVideo && (
        <div className="video-modal" onClick={closeVideo}>
          <div className="video-modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-modal" onClick={closeVideo}>
              ×
            </button>
            <div className="video-wrapper">
              <iframe
                src={selectedVideo}
                title="Event Video"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export default EventGlimpses;
