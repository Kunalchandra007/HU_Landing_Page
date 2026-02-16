import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminLogout, getEvents, getHappenings, deleteEvent, deleteHappening } from '../services/api';
import './AdminDashboard.css';

function AdminDashboard() {
  const [admin, setAdmin] = useState(null);
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState([]);
  const [happenings, setHappenings] = useState([]);
  const navigate = useNavigate();

  const checkAuth = useCallback(() => {
    try {
      // Check localStorage for login state
      const isLoggedIn = localStorage.getItem('adminLoggedIn');
      const username = localStorage.getItem('adminUsername');
      
      if (isLoggedIn === 'true' && username) {
        setAdmin({ username });
      } else {
        navigate('/admin/login');
      }
    } catch (error) {
      console.error('Auth check error:', error);
      navigate('/admin/login');
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  const fetchData = useCallback(async () => {
    try {
      const [eventsData, happeningsData] = await Promise.all([
        getEvents(),
        getHappenings()
      ]);
      setEvents(eventsData);
      setHappenings(happeningsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }, []);

  useEffect(() => {
    checkAuth();
    fetchData();
  }, [checkAuth, fetchData]);

  const handleLogout = async () => {
    try {
      // Clear localStorage
      localStorage.removeItem('adminLoggedIn');
      localStorage.removeItem('adminUsername');
      
      // Try to logout from backend (optional, don't wait for it)
      adminLogout().catch(() => {});
      
      navigate('/admin/login');
    } catch (error) {
      console.error('Logout error:', error);
      navigate('/admin/login');
    }
  };

  const handleMainWebsite = async () => {
    // Logout and redirect to main website
    localStorage.removeItem('adminLoggedIn');
    localStorage.removeItem('adminUsername');
    adminLogout().catch(() => {});
    window.location.href = '/';
  };

  const handleDeleteEvent = async (eventId) => {
    if (window.confirm('Are you sure you want to delete this event?')) {
      try {
        await deleteEvent(eventId);
        // Refresh events list
        fetchData();
        alert('Event deleted successfully!');
      } catch (error) {
        console.error('Error deleting event:', error);
        alert('Failed to delete event. Please try again.');
      }
    }
  };

  const handleDeleteHappening = async (happeningId) => {
    if (window.confirm('Are you sure you want to delete this happening?')) {
      try {
        await deleteHappening(happeningId);
        // Refresh happenings list
        fetchData();
        alert('Happening deleted successfully!');
      } catch (error) {
        console.error('Error deleting happening:', error);
        alert('Failed to delete happening. Please try again.');
      }
    }
  };

  if (loading) {
    return <div className="admin-dashboard"><p>Loading...</p></div>;
  }

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <div className="admin-info">
          <span>Welcome, {admin?.username}!</span>
          <button onClick={handleMainWebsite} className="main-website-btn">
            🏠 Main Website
          </button>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </div>
      
      <div className="dashboard-content">
        {/* Events Management Section */}
        <div className="dashboard-section">
          <div className="section-header">
            <h2>📅 Events Management</h2>
            <button className="add-btn" onClick={() => navigate('/admin/events/add')}>
              + Add Event
            </button>
          </div>
          
          <div className="items-grid">
            {events.length > 0 ? (
              events.map(event => (
                <div key={event.id} className="item-card">
                  <img src={`/${event.image_path}`} alt={event.title} />
                  <div className="item-info">
                    <h3>{event.title}</h3>
                    <p>{event.description.substring(0, 100)}...</p>
                    <span className="item-date">{event.event_date}</span>
                  </div>
                  <div className="item-actions">
                    <button className="edit-btn" onClick={() => navigate(`/admin/events/edit/${event.id}`)}>Edit</button>
                    <button className="delete-btn" onClick={() => handleDeleteEvent(event.id)}>Delete</button>
                  </div>
                </div>
              ))
            ) : (
              <p className="no-items">No events found. Add your first event!</p>
            )}
          </div>
        </div>

        {/* Happenings Management Section */}
        <div className="dashboard-section">
          <div className="section-header">
            <h2>📰 Happenings Management</h2>
            <button className="add-btn" onClick={() => navigate('/admin/happenings/add')}>
              + Add Happening
            </button>
          </div>
          
          <div className="items-grid">
            {happenings.length > 0 ? (
              happenings.map(happening => (
                <div key={happening.id} className="item-card">
                  <img src={`/${happening.image_path}`} alt={happening.title} />
                  <div className="item-info">
                    <h3>{happening.title}</h3>
                    <p>{happening.description.substring(0, 100)}...</p>
                  </div>
                  <div className="item-actions">
                    <button className="edit-btn" onClick={() => navigate(`/admin/happenings/edit/${happening.id}`)}>Edit</button>
                    <button className="delete-btn" onClick={() => handleDeleteHappening(happening.id)}>Delete</button>
                  </div>
                </div>
              ))
            ) : (
              <p className="no-items">No happenings found. Add your first happening!</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
