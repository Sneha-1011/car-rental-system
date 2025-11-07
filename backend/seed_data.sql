-- Car Rental System - Seed Data
-- This file contains sample data to populate the database

-- Create tables (SQLite syntax)
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    daily_rate REAL NOT NULL CHECK (daily_rate > 0),
    available BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS rentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
);

-- Insert sample cars
INSERT INTO cars (make, model, year, daily_rate, available) VALUES
    ('Toyota', 'Camry', 2023, 45.00, 1),
    ('Honda', 'Civic', 2022, 40.00, 1),
    ('Ford', 'Mustang', 2023, 75.00, 1),
    ('Tesla', 'Model 3', 2024, 95.00, 1),
    ('BMW', 'X5', 2023, 120.00, 1),
    ('Mercedes-Benz', 'C-Class', 2023, 110.00, 1),
    ('Audi', 'A4', 2022, 85.00, 1),
    ('Chevrolet', 'Malibu', 2021, 38.00, 1),
    ('Nissan', 'Altima', 2022, 42.00, 1),
    ('Hyundai', 'Elantra', 2023, 35.00, 1),
    ('Volkswagen', 'Jetta', 2022, 43.00, 1),
    ('Mazda', 'CX-5', 2023, 55.00, 1),
    ('Subaru', 'Outback', 2023, 60.00, 1),
    ('Jeep', 'Grand Cherokee', 2022, 70.00, 1),
    ('Kia', 'Forte', 2023, 37.00, 1);

-- Insert sample rentals (some active, some completed)
INSERT INTO rentals (car_id, user_name, start_date, end_date, rental_date) VALUES
    (1, 'John Doe', '2025-11-10 10:00:00', '2025-11-15 10:00:00', '2025-11-05 09:30:00'),
    (3, 'Jane Smith', '2025-11-08 14:00:00', '2025-11-12 14:00:00', '2025-11-04 11:20:00'),
    (5, 'Bob Johnson', '2025-11-20 09:00:00', '2025-11-25 09:00:00', '2025-11-06 08:15:00');

-- Update car availability based on active rentals
UPDATE cars SET available = 0 WHERE id IN (
    SELECT DISTINCT car_id FROM rentals 
    WHERE end_date > datetime('now')
);
