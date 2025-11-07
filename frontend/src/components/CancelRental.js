import React, { useState } from 'react';
import { rentalAPI } from '../services/api';
import './CancelRental.css';

const CancelRental = ({ onSuccess }) => {
  const [rentalId, setRentalId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await rentalAPI.cancelRental(parseInt(rentalId));
      setSuccess(result.message);
      setRentalId('');
      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to cancel rental. Please try again.';
      setError(errorMessage);
      console.error('Error canceling rental:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="cancel-rental-container">
      <h2>Cancel Rental</h2>
      <p className="description">Enter your rental ID to cancel a booking</p>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="rental_id">Rental ID *</label>
          <input
            type="number"
            id="rental_id"
            value={rentalId}
            onChange={(e) => setRentalId(e.target.value)}
            required
            placeholder="Enter rental ID"
            min="1"
          />
        </div>

        <button type="submit" disabled={loading || !rentalId} className="cancel-rental-btn">
          {loading ? 'Canceling...' : 'Cancel Rental'}
        </button>
      </form>
    </div>
  );
};

export default CancelRental;
