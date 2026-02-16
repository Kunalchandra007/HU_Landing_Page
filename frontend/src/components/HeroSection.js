import React from 'react';
import './HeroSection.css';

function HeroSection() {
  return (
    <section className="hero-section">
      {/* Video Background */}
      <div className="video-background">
        <iframe
          src="https://www.youtube.com/embed/blzl5ee5GSU?autoplay=1&mute=1&loop=1&playlist=blzl5ee5GSU&controls=0&modestbranding=1&fs=0"
          allow="autoplay; muted"
          title="Hero Video"
        />
      </div>

      {/* Logo */}
      <div className="hero-logo">
        <img src="/images/logo.jpeg" alt="Haridwar University Logo" />
      </div>

      {/* Top Right Buttons */}
      <div className="hero-nav-buttons">
        <a href="#about" className="nav-btn">About Us</a>
        <a href="#programs" className="nav-btn">Programs</a>
        <a href="https://huroorkee.ac.in/apply-now" target="_blank" rel="noopener noreferrer" className="nav-btn primary">
          Register Now
        </a>
      </div>

      {/* Hero Content */}
      <div className="hero-content">
        <div className="hero-text">
          <h1>ADMISSIONS 2026 OPEN</h1>
          <p>Join Haridwar University's programs, where innovation, technology, and values unite to shape a better tomorrow for all.</p>
          <a href="https://huroorkee.ac.in/apply-now" target="_blank" rel="noopener noreferrer" className="apply-btn">
            <span>+</span> Apply Now
          </a>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
