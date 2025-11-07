import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from main import app
from db import Base, get_db
import models

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create and clean database before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestCarEndpoints:
    """Test cases for car-related endpoints"""
    
    def test_create_car(self):
        """Test creating a new car"""
        response = client.post(
            "/cars/",
            json={
                "make": "Toyota",
                "model": "Camry",
                "year": 2023,
                "daily_rate": 45.0,
                "available": True
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["make"] == "Toyota"
        assert data["model"] == "Camry"
        assert data["id"] is not None
    
    def test_create_car_invalid_rate(self):
        """Test creating car with invalid daily rate"""
        response = client.post(
            "/cars/",
            json={
                "make": "Toyota",
                "model": "Camry",
                "year": 2023,
                "daily_rate": -10.0,  # Invalid negative rate
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_get_all_cars(self):
        """Test retrieving all cars"""
        # Create test cars
        client.post("/cars/", json={"make": "Toyota", "model": "Camry", "year": 2023, "daily_rate": 45.0})
        client.post("/cars/", json={"make": "Honda", "model": "Civic", "year": 2022, "daily_rate": 40.0})
        
        response = client.get("/cars/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_get_car_by_id(self):
        """Test retrieving a specific car"""
        # Create a car
        create_response = client.post(
            "/cars/",
            json={"make": "Ford", "model": "Mustang", "year": 2023, "daily_rate": 75.0}
        )
        car_id = create_response.json()["id"]
        
        # Get the car
        response = client.get(f"/cars/{car_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["make"] == "Ford"
        assert data["model"] == "Mustang"
    
    def test_get_nonexistent_car(self):
        """Test retrieving a car that doesn't exist"""
        response = client.get("/cars/999")
        assert response.status_code == 404


class TestRentalEndpoints:
    """Test cases for rental-related endpoints"""
    
    def test_rent_car_success(self):
        """Test successful car rental"""
        # Create a car
        car_response = client.post(
            "/cars/",
            json={"make": "Tesla", "model": "Model 3", "year": 2024, "daily_rate": 95.0}
        )
        car_id = car_response.json()["id"]
        
        # Rent the car
        start_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
        end_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
        
        response = client.post(
            f"/cars/{car_id}/rent",
            json={
                "user_name": "John Doe",
                "start_date": start_date,
                "end_date": end_date
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user_name"] == "John Doe"
        assert data["car_id"] == car_id
        assert "total_cost" in data
    
    def test_rent_nonexistent_car(self):
        """Test renting a car that doesn't exist"""
        start_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
        end_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
        
        response = client.post(
            "/cars/999/rent",
            json={
                "user_name": "John Doe",
                "start_date": start_date,
                "end_date": end_date
            }
        )
        assert response.status_code == 404
    
    def test_rent_car_past_date(self):
        """Test renting a car with past start date"""
        # Create a car
        car_response = client.post(
            "/cars/",
            json={"make": "BMW", "model": "X5", "year": 2023, "daily_rate": 120.0}
        )
        car_id = car_response.json()["id"]
        
        # Try to rent with past date
        past_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
        end_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
        
        response = client.post(
            f"/cars/{car_id}/rent",
            json={
                "user_name": "John Doe",
                "start_date": past_date,
                "end_date": end_date
            }
        )
        assert response.status_code == 400
    
    def test_rent_car_overlapping_dates(self):
        """Test renting a car with overlapping dates"""
        # Create a car
        car_response = client.post(
            "/cars/",
            json={"make": "Audi", "model": "A4", "year": 2022, "daily_rate": 85.0}
        )
        car_id = car_response.json()["id"]
        
        # First rental
        start_date1 = (datetime.utcnow() + timedelta(days=1)).isoformat()
        end_date1 = (datetime.utcnow() + timedelta(days=5)).isoformat()
        
        client.post(
            f"/cars/{car_id}/rent",
            json={
                "user_name": "John Doe",
                "start_date": start_date1,
                "end_date": end_date1
            }
        )
        
        # Try to rent same car with overlapping dates
        start_date2 = (datetime.utcnow() + timedelta(days=3)).isoformat()
        end_date2 = (datetime.utcnow() + timedelta(days=7)).isoformat()
        
        response = client.post(
            f"/cars/{car_id}/rent",
            json={
                "user_name": "Jane Smith",
                "start_date": start_date2,
                "end_date": end_date2
            }
        )
        assert response.status_code == 400
    
    def test_cancel_rental(self):
        """Test canceling a rental"""
        # Create a car and rental
        car_response = client.post(
            "/cars/",
            json={"make": "Mazda", "model": "CX-5", "year": 2023, "daily_rate": 55.0}
        )
        car_id = car_response.json()["id"]
        
        start_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
        end_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
        
        rental_response = client.post(
            f"/cars/{car_id}/rent",
            json={
                "user_name": "Bob Johnson",
                "start_date": start_date,
                "end_date": end_date
            }
        )
        rental_id = rental_response.json()["id"]
        
        # Cancel the rental
        response = client.delete(f"/rentals/{rental_id}")
        assert response.status_code == 200
        assert "successfully cancelled" in response.json()["message"]
    
    def test_cancel_nonexistent_rental(self):
        """Test canceling a rental that doesn't exist"""
        response = client.delete("/rentals/999")
        assert response.status_code == 404


class TestHealthChecks:
    """Test cases for health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "online"
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestBusinessLogic:
    """Test cases for business logic validation"""
    
    def test_car_availability_after_rental(self):
        """Test that car availability updates after rental"""
        # Create a car
        car_response = client.post(
            "/cars/",
            json={"make": "Hyundai", "model": "Elantra", "year": 2023, "daily_rate": 35.0}
        )
        car_id = car_response.json()["id"]
        
        # Rent the car
        start_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
        end_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
        
        client.post(
            f"/cars/{car_id}/rent",
            json={
                "user_name": "Alice Cooper",
                "start_date": start_date,
                "end_date": end_date
            }
        )
        
        # Check car availability
        car = client.get(f"/cars/{car_id}").json()
        assert car["available"] == False
    
    def test_car_availability_after_cancellation(self):
        """Test that car becomes available after rental cancellation"""
        # Create a car and rental
        car_response = client.post(
            "/cars/",
            json={"make": "Kia", "model": "Forte", "year": 2023, "daily_rate": 37.0}
        )
        car_id = car_response.json()["id"]
        
        start_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
        end_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
        
        rental_response = client.post(
            f"/cars/{car_id}/rent",
            json={
                "user_name": "Charlie Brown",
                "start_date": start_date,
                "end_date": end_date
            }
        )
        rental_id = rental_response.json()["id"]
        
        # Cancel the rental
        client.delete(f"/rentals/{rental_id}")
        
        # Check car availability
        car = client.get(f"/cars/{car_id}").json()
        assert car["available"] == True
