import React, { useState } from 'react';
import CarList from './components/CarList';
import RentCarForm from './components/RentCarForm';
import CancelRental from './components/CancelRental';
import './App.css';

function App() {
  const [selectedCar, setSelectedCar] = useState(null);
  const [activeTab, setActiveTab] = useState('browse');
  const [notification, setNotification] = useState(null);

  const handleRentClick = (car) => {
    setSelectedCar(car);
  };

  const handleCloseModal = () => {
    setSelectedCar(null);
  };

  const handleRentalSuccess = (rental) => {
    setSelectedCar(null);
    setNotification({
      type: 'success',
      message: `Successfully rented ${rental.car?.make} ${rental.car?.model}! Rental ID: ${rental.id}. Total cost: $${rental.total_cost.toFixed(2)}`
    });
    setTimeout(() => setNotification(null), 5000);
  };

  const handleCancelSuccess = () => {
    setNotification({
      type: 'success',
      message: 'Rental cancelled successfully!'
    });
    setTimeout(() => setNotification(null), 5000);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🚗 Car Rental System</h1>
        <p className="tagline">Find and rent your perfect car</p>
      </header>

      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}

      <nav className="tab-navigation">
        <button
          className={`tab-btn ${activeTab === 'browse' ? 'active' : ''}`}
          onClick={() => setActiveTab('browse')}
        >
          Browse Cars
        </button>
        <button
          className={`tab-btn ${activeTab === 'cancel' ? 'active' : ''}`}
          onClick={() => setActiveTab('cancel')}
        >
          Cancel Rental
        </button>
      </nav>

      <main className="app-content">
        {activeTab === 'browse' && (
          <CarList onRentClick={handleRentClick} />
        )}

        {activeTab === 'cancel' && (
          <CancelRental onSuccess={handleCancelSuccess} />
        )}
      </main>

      {selectedCar && (
        <RentCarForm
          car={selectedCar}
          onClose={handleCloseModal}
          onSuccess={handleRentalSuccess}
        />
      )}

      <footer className="app-footer">
        <p>&copy; 2025 Car Rental System. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
