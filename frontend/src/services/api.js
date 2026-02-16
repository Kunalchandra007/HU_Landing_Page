import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Events API
export const getEvents = async () => {
  const response = await api.get('/events');
  return response.data;
};

// Happenings API
export const getHappenings = async () => {
  const response = await api.get('/happenings');
  return response.data;
};

// Contact API
export const sendContactMessage = async (data) => {
  const response = await api.post('/contact', data);
  return response.data;
};

// Admin API
export const adminLogin = async (credentials) => {
  const response = await api.post('/admin/login', credentials);
  return response.data;
};

export const adminLogout = async () => {
  const response = await api.post('/admin/logout');
  return response.data;
};

export const getCurrentAdmin = async () => {
  const response = await api.get('/admin/me');
  return response.data;
};

// Add Event
export const addEvent = async (formData) => {
  const response = await api.post('/admin/events', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Add Happening
export const addHappening = async (formData) => {
  const response = await api.post('/admin/happenings', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Delete Event
export const deleteEvent = async (eventId) => {
  const response = await api.delete(`/admin/events/${eventId}`);
  return response.data;
};

// Delete Happening
export const deleteHappening = async (happeningId) => {
  const response = await api.delete(`/admin/happenings/${happeningId}`);
  return response.data;
};

// Get single event
export const getEvent = async (eventId) => {
  const response = await api.get(`/admin/events/${eventId}`);
  return response.data;
};

// Update event
export const updateEvent = async (eventId, formData) => {
  const response = await api.put(`/admin/events/${eventId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Get single happening
export const getHappening = async (happeningId) => {
  const response = await api.get(`/admin/happenings/${happeningId}`);
  return response.data;
};

// Update happening
export const updateHappening = async (happeningId, formData) => {
  const response = await api.put(`/admin/happenings/${happeningId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Mark event as completed
export const markEventCompleted = async (eventId, videoUrl) => {
  const response = await api.put(`/admin/events/${eventId}/complete`, { video_url: videoUrl });
  return response.data;
};

// Mark happening as completed
export const markHappeningCompleted = async (happeningId) => {
  const response = await api.put(`/admin/happenings/${happeningId}/complete`);
  return response.data;
};

// Get completed events
export const getCompletedEvents = async () => {
  const response = await api.get('/events/completed');
  return response.data;
};

export default api;
