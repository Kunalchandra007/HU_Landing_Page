import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getHappening, updateHappening } from '../services/api';
import './AddContent.css';

function EditHappening() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    image: null
  });
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(true);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState(null);
  const [currentImage, setCurrentImage] = useState(null);

  useEffect(() => {
    const fetchHappening = async () => {
      try {
        const happening = await getHappening(id);
        setFormData({
          title: happening.title,
          description: happening.description,
          image: null
        });
        setCurrentImage(happening.image_path);
      } catch (err) {
        console.error('Error fetching happening:', err);
        setError('Failed to load happening data');
      } finally {
        setFetchLoading(false);
      }
    };

    fetchHappening();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        image: file
      }));
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('title', formData.title);
      formDataToSend.append('description', formData.description);
      if (formData.image) {
        formDataToSend.append('image', formData.image);
      }

      const response = await updateHappening(id, formDataToSend);
      console.log('Happening updated:', response);
      
      alert('Happening updated successfully!');
      navigate('/admin/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update happening. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (fetchLoading) {
    return (
      <div className="add-content-page">
        <div className="add-content-container">
          <p>Loading happening data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="add-content-page">
      <div className="add-content-container">
        <div className="page-header">
          <button onClick={() => navigate('/admin/dashboard')} className="back-btn">
            ← Back to Dashboard
          </button>
          <h1>✏️ Edit Happening</h1>
        </div>

        <form onSubmit={handleSubmit} className="content-form">
          <div className="form-group">
            <label htmlFor="title">Happening Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Enter happening title"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Happening Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter happening description"
              rows="5"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="image">Happening Image (leave empty to keep current)</label>
            <input
              type="file"
              id="image"
              name="image"
              onChange={handleImageChange}
              accept="image/*"
            />
            {preview ? (
              <div className="image-preview">
                <p>New Image:</p>
                <img src={preview} alt="Preview" />
              </div>
            ) : currentImage ? (
              <div className="image-preview">
                <p>Current Image:</p>
                <img src={`/${currentImage}`} alt="Current" />
              </div>
            ) : null}
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="form-actions">
            <button type="button" onClick={() => navigate('/admin/dashboard')} className="cancel-btn">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Updating...' : 'Update Happening'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EditHappening;
