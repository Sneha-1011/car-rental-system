# Car Rental System - Manual Installation Guide

## Prerequisites

- Python 3.10 or higher
- Node.js 14 or higher
- Google Cloud account
- `credentials.json` file in the project root directory

## 0. Firestore Database Setup (REQUIRED - First Time Only)

⚠️ **You must create a Firestore database before running the application!**

### Create Firestore Database

1. **Open the Firestore setup page** for your project:
   ```
   https://console.cloud.google.com/datastore/setup?project=skill-sync-ai-472908
   ```

2. **Select "Firestore Native Mode"**
   - Do NOT choose "Datastore Mode"

3. **Choose a location** (e.g., `us-central1`, `us-east1`)
   - This cannot be changed later!

4. **Click "Create Database"**
   - Wait 1-2 minutes for creation to complete

5. **Verify creation**:
   - Go to: https://console.cloud.google.com/firestore/data?project=skill-sync-ai-472908
   - You should see an empty database

📖 **For detailed instructions, see [FIRESTORE_SETUP.md](FIRESTORE_SETUP.md)**

## 1. Backend Setup

### Navigate to backend directory
```cmd
cd "c:\Users\HP\Downloads\Car Rental\backend"
```

### Create virtual environment
```cmd
python -m venv venv
```

### Activate virtual environment
```cmd
venv\Scripts\activate
```

### Install Python dependencies
```cmd
pip install -r requirements.txt
```

### Seed Firestore with sample data
```cmd
python seed_firestore.py
```

This will add 15 sample cars to your Firestore database.

## 2. Frontend Setup

### Open a new terminal and navigate to frontend directory
```cmd
cd "c:\Users\HP\Downloads\Car Rental\frontend"
```

### Install Node.js dependencies
```cmd
npm install
```

## 3. Running the Application

### Start Backend (Terminal 1)
```cmd
cd "c:\Users\HP\Downloads\Car Rental\backend"
venv\Scripts\activate
uvicorn main:app --reload
```

The backend will start on http://localhost:8000

### Start Frontend (Terminal 2)
```cmd
cd "c:\Users\HP\Downloads\Car Rental\frontend"
npm start
```

The frontend will start on http://localhost:3000

## 4. Access Points

- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API (Swagger UI)**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## 5. Verify Installation

### Check Backend Health
Open http://localhost:8000/health in your browser. You should see:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Check Frontend
Open http://localhost:3000 and you should see the list of available cars.

## 6. Database Information

### Firestore Collections

- **cars**: Stores all vehicle information
  - Fields: make, model, year, daily_rate, available, created_at
  
- **rentals**: Stores rental bookings
  - Fields: car_id, user_name, start_date, end_date, rental_date

### View Data in Firestore Console

1. Go to https://console.cloud.google.com/firestore
2. Select your project
3. View the `cars` and `rentals` collections

## 7. Running Tests (Optional)

### Backend Tests
```cmd
cd "c:\Users\HP\Downloads\Car Rental\backend"
venv\Scripts\activate
pytest
```

## Troubleshooting

### Backend won't start
- Ensure `credentials.json` exists in the root directory
- Check that your Google Cloud project has Firestore enabled
- Verify Python version: `python --version` (should be 3.10+)

### Frontend won't start
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall: `rmdir /s node_modules && npm install`
- Check Node version: `node --version` (should be 14+)

### No cars showing in frontend
- Run the seed script: `python seed_firestore.py`
- Check Firestore console to verify data exists
- Check browser console for errors (F12)

### CORS errors
- Ensure backend is running on port 8000
- Check that CORS middleware is properly configured in `main.py`

## Next Steps

1. **Add more cars**: Use the API docs at http://localhost:8000/docs to add cars via POST /cars/
2. **Rent a car**: Click on any car in the frontend and fill out the rental form
3. **View rentals**: Check the rentals collection in Firestore console
4. **Cancel rentals**: Use the cancel button in the UI or DELETE /rentals/{id} endpoint

## Environment Variables (Optional)

Create a `.env` file in the backend directory for configuration:

```env
# Firestore configuration
GOOGLE_APPLICATION_CREDENTIALS=../credentials.json

# API configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info
```

## Production Deployment

For production deployment:

1. Update CORS origins in `main.py` to specific domains
2. Set up proper authentication and authorization
3. Configure Firestore security rules
4. Use environment variables for sensitive configuration
5. Enable HTTPS
6. Set up monitoring and logging

## Support

For issues or questions:
- Check the API documentation at http://localhost:8000/docs
- Review Firestore logs in Google Cloud Console
- Check application logs in terminal output
