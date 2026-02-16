import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Contact from './pages/Contact';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import AddEvent from './pages/AddEvent';
import AddHappening from './pages/AddHappening';
import EditEvent from './pages/EditEvent';
import EditHappening from './pages/EditHappening';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/admin/events/add" element={<AddEvent />} />
          <Route path="/admin/events/edit/:id" element={<EditEvent />} />
          <Route path="/admin/happenings/add" element={<AddHappening />} />
          <Route path="/admin/happenings/edit/:id" element={<EditHappening />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
