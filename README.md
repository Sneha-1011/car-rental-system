# 🚗 Car Rental System

A comprehensive full-stack car rental management system built with FastAPI, ReactJS, and Google Cloud SQL, featuring automated SDK generation and complete CI/CD support.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Running Tests](#running-tests)
- [SDK Generation](#sdk-generation)
- [API Documentation](#api-documentation)
- [Business Logic](#business-logic)
- [Google Cloud Integration](#google-cloud-integration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

The Car Rental System is a modern, production-ready application that allows users to:
- Browse available cars for rent
- Rent cars for specific time periods
- Cancel rental bookings
- Manage car inventory

The system implements sophisticated business logic including date overlap validation, availability management, and automatic cost calculation.

## ✨ Features

### Backend (FastAPI)
- ✅ **RESTful API** with OpenAPI 3.0 specification
- ✅ **Automatic validation** using Pydantic models
- ✅ **Database management** with SQLAlchemy ORM
- ✅ **Google Cloud SQL** integration (PostgreSQL)
- ✅ **SQLite fallback** for local development
- ✅ **CORS support** for cross-origin requests
- ✅ **Comprehensive error handling**
- ✅ **Unit tests** with pytest
- ✅ **Interactive API documentation** (Swagger UI)

### Frontend (ReactJS)
- ✅ **Modern, responsive UI** with React 18
- ✅ **Component-based architecture**
- ✅ **Real-time car availability** updates
- ✅ **Date validation** and cost estimation
- ✅ **Error handling** and user notifications
- ✅ **Axios-based API integration**

### Business Logic
- ✅ **Rental overlap prevention** - Cars cannot be double-booked
- ✅ **Automatic availability management** - Cars marked unavailable when rented
- ✅ **Date validation** - No past dates, end date after start date
- ✅ **Dynamic pricing** - Cost calculated based on rental duration
- ✅ **Cancellation handling** - Cars become available after cancellation

### DevOps & Tooling
- ✅ **Automated setup** with PowerShell scripts
- ✅ **SDK generation** using OpenAPI Generator CLI
- ✅ **Database seeding** with sample data
- ✅ **Environment configuration** support
- ✅ **Comprehensive documentation**

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 (SQLite/PostgreSQL)
- **Cloud**: Google Cloud SQL, Vertex AI
- **Validation**: Pydantic 2.5.0
- **Testing**: pytest 7.4.3
- **Server**: Uvicorn 0.24.0

### Frontend
- **Framework**: React 18.2.0
- **HTTP Client**: Axios 1.6.2
- **Build Tool**: React Scripts 5.0.1
- **Styling**: CSS3

### Tools
- **API Documentation**: Swagger UI / ReDoc
- **SDK Generator**: OpenAPI Generator CLI
- **Database Client**: pg8000 (PostgreSQL)
- **Automation**: PowerShell

## 📁 Project Structure

```
Car Rental/
├── backend/
│   ├── db.py                 # Database configuration
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── routes.py             # API routes
│   ├── main.py               # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── seed_data.sql         # Database seed data
│   └── test_main.py          # Unit tests
├── frontend/
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── CarList.js    # Car listing component
│   │   │   ├── CarList.css
│   │   │   ├── RentCarForm.js # Rental form component
│   │   │   ├── RentCarForm.css
│   │   │   ├── CancelRental.js # Cancellation component
│   │   │   └── CancelRental.css
│   │   ├── services/
│   │   │   └── api.js        # API service layer
│   │   ├── App.js            # Main App component
│   │   ├── App.css
│   │   ├── index.js          # React entry point
│   │   └── index.css
│   └── package.json          # Node dependencies
├── credentials.json          # Google Cloud credentials
├── setup.ps1                 # Setup automation script
├── run.ps1                   # Run automation script
├── SDK_GENERATION.md         # SDK generation guide
└── README.md                 # This file
```

## 📦 Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Git** - [Download](https://git-scm.com/)
- **Google Cloud Account** (optional, for Cloud SQL)

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Clone or navigate to the project directory**:
   ```powershell
   cd "C:\Users\HP\Downloads\Car Rental"
   ```

2. **Run the setup script**:
   ```powershell
   .\setup.ps1
   ```

3. **Start the application**:
   ```powershell
   .\run.ps1
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

See [Detailed Setup](#detailed-setup) below.

## 🔧 Detailed Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```powershell
   cd backend
   ```

2. **Create virtual environment**:
   ```powershell
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

5. **Initialize database** (SQLite for local development):
   ```powershell
   # Using Python
   python -c "import sqlite3, sys; conn = sqlite3.connect('car_rental.db'); conn.executescript(open('seed_data.sql').read()); conn.commit(); conn.close()"
   ```

6. **Run the backend**:
   ```powershell
   python main.py
   ```

   The API will be available at http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**:
   ```powershell
   cd frontend
   ```

2. **Install dependencies**:
   ```powershell
   npm install
   ```

3. **Start the development server**:
   ```powershell
   npm start
   ```

   The frontend will open automatically at http://localhost:3000

## 🧪 Running Tests

### Backend Tests

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest test_main.py -v
```

### Run tests with coverage:

```powershell
pytest test_main.py -v --cov=. --cov-report=html
```

### Test Categories

The test suite includes:
- ✅ **Car CRUD operations** (Create, Read, Update, Delete)
- ✅ **Rental creation** with validation
- ✅ **Overlap detection** for date conflicts
- ✅ **Cancellation logic**
- ✅ **Availability management**
- ✅ **Error handling** (404, 400, 422)

## 📚 SDK Generation

Generate a Python SDK for the Car Rental API:

### 1. Install OpenAPI Generator CLI

```powershell
npm install -g @openapitools/openapi-generator-cli
```

### 2. Ensure Backend is Running

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

### 3. Generate SDK

```powershell
# From project root
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o car_rental_sdk --package-name car_rental_client
```

### 4. Install and Use SDK

```powershell
cd car_rental_sdk
pip install -e .
```

For detailed SDK usage examples, see [SDK_GENERATION.md](SDK_GENERATION.md)

## 📖 API Documentation

### Interactive Documentation

Once the backend is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### API Endpoints

#### Cars

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cars/` | Add a new car |
| GET | `/cars/` | Get all cars |
| GET | `/cars/{car_id}` | Get specific car |
| POST | `/cars/{car_id}/rent` | Rent a car |

#### Rentals

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rentals/` | Get all rentals |
| GET | `/rentals/{rental_id}` | Get specific rental |
| DELETE | `/rentals/{rental_id}` | Cancel a rental |

#### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |

### Example Requests

#### Add a Car

```bash
curl -X POST "http://localhost:8000/cars/" \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Toyota",
    "model": "Camry",
    "year": 2023,
    "daily_rate": 45.0,
    "available": true
  }'
```

#### Rent a Car

```bash
curl -X POST "http://localhost:8000/cars/1/rent" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John Doe",
    "start_date": "2025-11-10T10:00:00",
    "end_date": "2025-11-15T10:00:00"
  }'
```

#### Cancel a Rental

```bash
curl -X DELETE "http://localhost:8000/rentals/1"
```

## 🧠 Business Logic

### Rental Validation

The system implements sophisticated validation rules:

1. **Date Overlap Prevention**
   - Checks all existing rentals for the requested car
   - Prevents bookings if dates overlap
   - Returns 400 error with descriptive message

2. **Date Validation**
   - Start date must be in the future
   - End date must be after start date
   - Enforced at both schema and route levels

3. **Availability Management**
   - Cars marked unavailable when rented
   - Automatically updated on cancellation
   - Tracks based on active/upcoming rentals

4. **Cost Calculation**
   - `Total Cost = Daily Rate × Number of Days`
   - Minimum 1 day rental
   - Returned with rental confirmation

### Database Schema

#### Cars Table
```sql
CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    daily_rate REAL NOT NULL CHECK (daily_rate > 0),
    available BOOLEAN NOT NULL DEFAULT 1
);
```

#### Rentals Table
```sql
CREATE TABLE rentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
);
```

## ☁️ Google Cloud Integration

The system supports Google Cloud SQL (PostgreSQL) for production deployments.

### Setup Google Cloud SQL

1. **Update database configuration** in `backend/db.py`:
   ```python
   INSTANCE_CONNECTION_NAME = "your-project:region:instance-name"
   DB_USER = "your-db-user"
   DB_PASS = "your-db-password"
   DB_NAME = "car_rental"
   ```

2. **Set environment variable**:
   ```powershell
   $env:USE_CLOUD_SQL = "true"
   ```

3. **Ensure credentials.json** is in the project root

4. **Run the application** - it will automatically use Cloud SQL

### Local Development Mode

By default, the system uses SQLite for easy local development. No configuration needed!

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `Import "fastapi" could not be resolved`
- **Solution**: Activate virtual environment and install dependencies
  ```powershell
  cd backend
  .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

**Issue**: Database not found
- **Solution**: Run seed data script
  ```powershell
  python -c "import sqlite3; conn = sqlite3.connect('car_rental.db'); conn.executescript(open('seed_data.sql').read()); conn.commit()"
  ```

**Issue**: Port 8000 already in use
- **Solution**: Find and kill the process or use a different port
  ```powershell
  # Find process
  netstat -ano | findstr :8000
  # Kill process (replace PID)
  taskkill /PID <PID> /F
  ```

### Frontend Issues

**Issue**: `npm install` fails
- **Solution**: Clear npm cache and retry
  ```powershell
  npm cache clean --force
  npm install
  ```

**Issue**: CORS errors
- **Solution**: Ensure backend is running and CORS is configured in `main.py`

**Issue**: API connection refused
- **Solution**: Verify backend is running on port 8000

### SDK Generation Issues

**Issue**: OpenAPI Generator not found
- **Solution**: Install globally
  ```powershell
  npm install -g @openapitools/openapi-generator-cli
  ```

**Issue**: Cannot access OpenAPI spec
- **Solution**: Ensure backend is running before generating SDK

## 📝 Environment Variables

Create a `.env` file in the backend directory (optional):

```env
# Database Configuration
USE_CLOUD_SQL=false

# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
INSTANCE_CONNECTION_NAME=your-project:region:instance

# Database Credentials
DB_USER=postgres
DB_PASS=your-password
DB_NAME=car_rental

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## 🎨 Customization

### Adding New Car Fields

1. Update `backend/models.py` - Add column to `Car` model
2. Update `backend/schemas.py` - Add field to schemas
3. Update `backend/seed_data.sql` - Include in sample data
4. Update `frontend/src/components/CarList.js` - Display new field

### Changing API Port

In `backend/main.py`:
```python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)  # Changed to 8080
```

In `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8080';  // Match backend port
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the frontend library
- Google Cloud for cloud infrastructure
- OpenAPI Generator for SDK generation

## 📞 Support

For issues, questions, or contributions:
- Create an issue in the repository
- Check existing documentation
- Review API documentation at `/docs`

---

**Built with ❤️ using FastAPI, React, and Google Cloud**
