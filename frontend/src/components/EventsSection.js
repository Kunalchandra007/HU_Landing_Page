import React, { useState } from 'react';
import './EventsSection.css';

function EventsSection({ events }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const eventsPerPage = 4;

  // Default events with DJ Night first
  const defaultEvents = [
    {
      id: 1,
      title: 'DJ Night',
      description: "let's groove to music and break the floor. This message is for all come and lets slay the dance the moves on the floor together and make this valentine dreamy.",
      event_date: '2026-02-14',
      image_path: '/images/djnight.jpeg'
    },
    {
      id: 2,
      title: 'Canvas Competition',
      description: 'Unleash your creativity in this exciting canvas art competition. Showcase your artistic talent and win amazing prizes...',
      event_date: '2026-02-14',
      image_path: '/images/canvacomp.jpeg'
    },
    {
      id: 3,
      title: 'Photography Competition',
      description: 'Capture the essence of moments. Participate in our photography competition and exhibit your best work...',
      event_date: '2026-02-14',
      image_path: '/images/photographycomp.jpeg'
    },
    {
      id: 4,
      title: 'Ramp Walk',
      description: 'Showcase fashion and style on the ramp. A glamorous event featuring latest trends and talented models...',
      event_date: '2026-02-15',
      image_path: '/images/rampwalk.jpeg'
    }
  ];

  const displayEvents = Array.isArray(events) && events.length > 0 ? events : defaultEvents;

  const handlePrev = () => {
    setCurrentIndex((prev) => {
      const newIndex = prev - 1;
      return newIndex < 0 ? Math.max(0, displayEvents.length - eventsPerPage) : newIndex;
    });
  };

  const handleNext = () => {
    setCurrentIndex((prev) => {
      const newIndex = prev + 1;
      const maxIndex = Math.max(0, displayEvents.length - eventsPerPage);
      return newIndex > maxIndex ? 0 : newIndex;
    });
  };

  const visibleEvents = displayEvents.slice(currentIndex, currentIndex + eventsPerPage);
  const canGoPrev = currentIndex > 0;
  const canGoNext = currentIndex < displayEvents.length - eventsPerPage;

  return (
    <section className="events-section">
      <div className="events-container">
        <h2 className="events-title">UPCOMING EVENTS</h2>
        <div className="events-grid">
          {visibleEvents.map((event) => {
            const eventDate = new Date(event.event_date);
            const day = eventDate.getDate();
            const month = eventDate.toLocaleDateString('en-US', { month: 'short' }).toUpperCase();
            
            return (
              <div key={event.id} className="event-card">
                <div className="event-image-wrapper">
                  <img 
                    src={event.image_path} 
                    alt={event.title}
                    onError={(e) => {
                      console.error('Image failed to load:', event.image_path);
                      e.target.style.border = '2px solid red';
                    }}
                    onLoad={(e) => {
                      console.log('Image loaded successfully:', event.image_path);
                    }}
                  />
                  <div className="event-date-badge">
                    <span className="date-day">{day}</span>
                    <span className="date-month">{month}</span>
                  </div>
                </div>
                <div className="event-content">
                  <h3>{event.title}</h3>
                  <p>{event.description}</p>
                </div>
              </div>
            );
          })}
        </div>
        <div className="events-navigation">
          <button 
            className="nav-arrow" 
            onClick={handlePrev}
            disabled={!canGoPrev}
          >
            ←
          </button>
          <button 
            className="nav-arrow" 
            onClick={handleNext}
            disabled={!canGoNext}
          >
            →
          </button>
        </div>
      </div>
    </section>
  );
}

export default EventsSection;
