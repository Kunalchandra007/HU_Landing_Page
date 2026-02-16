import React, { useState, useEffect } from 'react';
import './HeroSection.css';

function HeroSection() {
  const [videoLoaded, setVideoLoaded] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Preload the fallback image
    const img = new Image();
    img.src = '/images/hero-fallback.avif';
    img.onload = () => setImageLoaded(true);

    // Keep fallback image for 5 seconds before showing video
    const timer = setTimeout(() => {
      setVideoLoaded(true);
    }, 5000); // Show fallback for exactly 5 seconds

    return () => clearTimeout(timer);
  }, []);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  return (
    <section className="hero-section">
      {/* Loading Spinner */}
      {!imageLoaded && (
        <div className="hero-loading">
          <div className="spinner"></div>
        </div>
      )}

      {/* Fallback Background Image */}
      <div className={`fallback-background ${videoLoaded ? 'fade-out' : ''} ${imageLoaded ? 'loaded' : ''}`}>
        <img src="/images/hero-fallback.avif" alt="Haridwar University" />
      </div>

      {/* Video Background */}
      <div className={`video-background ${videoLoaded ? 'fade-in' : ''}`}>
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

      {/* Mobile Menu Toggle Button */}
      <button 
        className={`mobile-menu-toggle ${mobileMenuOpen ? 'open' : ''}`}
        onClick={toggleMobileMenu}
        aria-label="Toggle menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Top Right Buttons - Desktop */}
      <div className="hero-nav-buttons desktop-nav">
        <a href="#about" className="nav-btn">About Us</a>
        <a href="#programs" className="nav-btn">Programs</a>
        <a href="https://huroorkee.ac.in/apply-now" target="_blank" rel="noopener noreferrer" className="nav-btn primary">
          Register Now
        </a>
      </div>

      {/* Mobile Menu Overlay */}
      <div className={`mobile-menu-overlay ${mobileMenuOpen ? 'open' : ''}`} onClick={closeMobileMenu}></div>

      {/* Mobile Menu */}
      <div className={`mobile-menu ${mobileMenuOpen ? 'open' : ''}`}>
        <div className="mobile-menu-header">
          <h3>Menu</h3>
          <button className="close-btn" onClick={closeMobileMenu} aria-label="Close menu">
            ×
          </button>
        </div>
        <nav className="mobile-menu-nav">
          <a href="#about" className="mobile-nav-link" onClick={closeMobileMenu}>
            <span className="icon">ℹ️</span>
            About Us
          </a>
          <a href="#programs" className="mobile-nav-link" onClick={closeMobileMenu}>
            <span className="icon">📚</span>
            Programs
          </a>
          <a 
            href="https://huroorkee.ac.in/apply-now" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="mobile-nav-link primary"
            onClick={closeMobileMenu}
          >
            <span className="icon">✓</span>
            Register Now
          </a>
        </nav>
      </div>

      {/* Hero Content */}
      <div className="hero-content">
        <div className="hero-text">
          {/* Admissions Badge */}
          <div className="admissions-badge">
            <span className="badge-icon">✦</span>
            <span className="badge-text">ADMISSIONS 2026 OPEN</span>
          </div>

          {/* Main Heading */}
          <div className="hero-title-wrapper">
            <h1 className="hero-main-title">
              <span className="title-white">ADMISSIONS</span>
              <span className="title-green">OPEN 2026</span>
            </h1>
          </div>

          {/* Description */}
          <p className="hero-description">
            Join Haridwar University, Uttarakhand's premier destination for future leaders. Experience state-of-the-art infrastructure and India's leading placement ecosystem with 100% career support.
          </p>

          {/* Action Buttons */}
          <div className="hero-buttons">
            <a href="https://huroorkee.ac.in/apply-now" target="_blank" rel="noopener noreferrer" className="hero-btn apply-now-btn">
              APPLY NOW
              <span className="btn-arrow">→</span>
            </a>
            <a href="https://huroorkee.ac.in/student-corner/photo-gallery" target="_blank" rel="noopener noreferrer" className="hero-btn campus-tour-btn">
              CAMPUS TOUR
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
