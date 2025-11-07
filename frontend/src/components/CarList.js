import React, { useState, useEffect } from 'react';
import { carAPI } from '../services/api';
import './CarList.css';

const CarList = ({ onRentClick }) => {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAvailableOnly, setShowAvailableOnly] = useState(false);

  const fetchCars = async () => {
    try {
      setLoading(true);
      const data = await carAPI.getAllCars(showAvailableOnly);
      setCars(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch cars. Please try again later.');
      console.error('Error fetching cars:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCars();
  }, [showAvailableOnly]);

  if (loading) {
    return <div className="loading">Loading cars...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="car-list-container">
      <div className="car-list-header">
        <h2>Available Cars</h2>
        <div className="filter-controls">
          <label>
            <input
              type="checkbox"
              checked={showAvailableOnly}
              onChange={(e) => setShowAvailableOnly(e.target.checked)}
            />
            Show available only
          </label>
          <button onClick={fetchCars} className="refresh-btn">
            🔄 Refresh
          </button>
        </div>
      </div>

      {cars.length === 0 ? (
        <p className="no-cars">No cars found.</p>
      ) : (
        <div className="car-grid">
          {cars.map((car) => (
            <div key={car.id} className={`car-card ${!car.available ? 'unavailable' : ''}`}>
              <div className="car-info">
                <h3>{car.make} {car.model}</h3>
                <p className="car-year">Year: {car.year}</p>
                <p className="car-rate">${car.daily_rate}/day</p>
                <p className={`car-status ${car.available ? 'available' : 'rented'}`}>
                  {car.available ? '✓ Available' : '✗ Currently Rented'}
                </p>
              </div>
              <div className="car-actions">
                <button
                  onClick={() => onRentClick(car)}
                  disabled={!car.available}
                  className="rent-btn"
                >
                  {car.available ? 'Rent This Car' : 'Not Available'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CarList;
