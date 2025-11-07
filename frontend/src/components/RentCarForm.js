import React, { useState } from 'react';
import { carAPI } from '../services/api';
import './RentCarForm.css';

const RentCarForm = ({ car, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    user_name: '',
    start_date: '',
    end_date: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [estimatedCost, setEstimatedCost] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Calculate estimated cost when dates change
    if (name === 'start_date' || name === 'end_date') {
      const start = name === 'start_date' ? new Date(value) : new Date(formData.start_date);
      const end = name === 'end_date' ? new Date(value) : new Date(formData.end_date);
      
      if (start && end && end > start) {
        const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
        setEstimatedCost(days * car.daily_rate);
      } else {
        setEstimatedCost(null);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Convert dates to ISO format
      const rentalData = {
        user_name: formData.user_name,
        start_date: new Date(formData.start_date).toISOString(),
        end_date: new Date(formData.end_date).toISOString(),
      };

      const result = await carAPI.rentCar(car.id, rentalData);
      onSuccess(result);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to rent car. Please try again.';
      setError(errorMessage);
      console.error('Error renting car:', err);
    } finally {
      setLoading(false);
    }
  };

  // Get today's date for min date validation
  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Rent {car.make} {car.model}</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="car-details">
          <p><strong>Year:</strong> {car.year}</p>
          <p><strong>Daily Rate:</strong> ${car.daily_rate}</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="user_name">Your Name *</label>
            <input
              type="text"
              id="user_name"
              name="user_name"
              value={formData.user_name}
              onChange={handleChange}
              required
              placeholder="Enter your full name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="start_date">Start Date *</label>
            <input
              type="datetime-local"
              id="start_date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
              min={today}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="end_date">End Date *</label>
            <input
              type="datetime-local"
              id="end_date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
              min={formData.start_date || today}
              required
            />
          </div>

          {estimatedCost !== null && (
            <div className="estimated-cost">
              <strong>Estimated Total Cost:</strong> ${estimatedCost.toFixed(2)}
            </div>
          )}

          <div className="form-actions">
            <button type="button" onClick={onClose} className="cancel-btn">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Processing...' : 'Confirm Rental'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RentCarForm;
