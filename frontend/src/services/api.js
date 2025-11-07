import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Car API calls
export const carAPI = {
  // Get all cars
  getAllCars: async (availableOnly = false) => {
    const response = await api.get('/cars/', {
      params: { available_only: availableOnly }
    });
    return response.data;
  },

  // Get a specific car
  getCar: async (carId) => {
    const response = await api.get(`/cars/${carId}`);
    return response.data;
  },

  // Add a new car
  addCar: async (carData) => {
    const response = await api.post('/cars/', carData);
    return response.data;
  },

  // Rent a car
  rentCar: async (carId, rentalData) => {
    const response = await api.post(`/cars/${carId}/rent`, rentalData);
    return response.data;
  },
};

// Rental API calls
export const rentalAPI = {
  // Get all rentals
  getAllRentals: async () => {
    const response = await api.get('/rentals/');
    return response.data;
  },

  // Get a specific rental
  getRental: async (rentalId) => {
    const response = await api.get(`/rentals/${rentalId}`);
    return response.data;
  },

  // Cancel a rental
  cancelRental: async (rentalId) => {
    const response = await api.delete(`/rentals/${rentalId}`);
    return response.data;
  },
};

export default api;
