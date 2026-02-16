import React, { useState, useEffect } from 'react';
import { getEvents, getHappenings } from '../services/api';
import HeroSection from '../components/HeroSection';
import AboutSection from '../components/AboutSection';
import AccreditationsSection from '../components/AccreditationsSection';
import ProgramsSection from '../components/ProgramsSection';
import SportsGallery from '../components/SportsGallery';
import WhySection from '../components/WhySection';
import HappeningsSection from '../components/HappeningsSection';
import EventsSection from '../components/EventsSection';
import AlumniCorner from '../components/AlumniCorner';
import Footer from '../components/Footer';

function Home() {
  const [events, setEvents] = useState([]);
  const [happenings, setHappenings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [eventsData, happeningsData] = await Promise.all([
          getEvents(),
          getHappenings()
        ]);
        setEvents(eventsData);
        setHappenings(happeningsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="home">
      <HeroSection />
      <AboutSection />
      <AccreditationsSection />
      <SportsGallery />
      <ProgramsSection />
      <WhySection />
      <HappeningsSection happenings={happenings} />
      <EventsSection events={events} />
      <AlumniCorner />
      <Footer />
    </div>
  );
}

export default Home;
