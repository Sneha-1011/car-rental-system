# Car Rental System - Quick Start

## 🚀 What You Need to Do Now

### Step 1: Create Firestore Database (5 minutes)

**Your project**: `skill-sync-ai-472908`

1. Click this link: https://console.cloud.google.com/datastore/setup?project=skill-sync-ai-472908

2. Select **"Firestore Native Mode"**

3. Choose location: **us-central1** (recommended)

4. Click **"Create Database"**

5. Wait for completion (1-2 minutes)

### Step 2: Install and Seed (5 minutes)

Open terminal and run:

```cmd
cd "c:\Users\HP\Downloads\Car Rental\backend"
venv\Scripts\activate
pip install google-cloud-firestore
python seed_firestore.py
```

You should see:
```
✅ Successfully added 15 cars to Firestore!
```

### Step 3: Start Application (1 minute)

**Terminal 1 - Backend**:
```cmd
cd "c:\Users\HP\Downloads\Car Rental\backend"
venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend**:
```cmd
cd "c:\Users\HP\Downloads\Car Rental\frontend"
npm start
```

### Step 4: Access Application

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Firestore Console**: https://console.cloud.google.com/firestore/data?project=skill-sync-ai-472908

## ✅ What's Changed

### Database Migration: SQLite/Cloud SQL → Firestore

**Removed**:
- ❌ SQLAlchemy ORM
- ❌ models.py
- ❌ Cloud SQL Connector
- ❌ PostgreSQL dependencies
- ❌ seed_data.sql

**Added**:
- ✅ Google Cloud Firestore (NoSQL)
- ✅ seed_firestore.py (Python seed script)
- ✅ Direct Firestore client
- ✅ Real-time data capabilities
- ✅ Automatic scaling

### Updated Files

1. **backend/db.py** - Now uses Firestore client instead of SQLAlchemy
2. **backend/routes.py** - Updated all CRUD operations for Firestore
3. **backend/main.py** - Removed SQLAlchemy table creation
4. **backend/requirements.txt** - Replaced SQL packages with Firestore
5. **backend/seed_firestore.py** - New seeding script

### Architecture

```
┌─────────────────┐
│   React App     │  (Port 3000)
│   (Frontend)    │
└────────┬────────┘
         │
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │  (Port 8000)
│   (Backend)     │
└────────┬────────┘
         │
         │ Firestore SDK
         ▼
┌─────────────────┐
│  Google         │  (Cloud)
│  Firestore      │
└─────────────────┘
```

## 📊 Firestore Collections

### cars
```json
{
  "make": "Toyota",
  "model": "Camry",
  "year": 2022,
  "daily_rate": 45.00,
  "available": true,
  "created_at": "2024-11-07T10:30:00Z"
}
```

### rentals
```json
{
  "car_id": "firestore_document_id",
  "user_name": "John Doe",
  "start_date": "2024-11-10T00:00:00Z",
  "end_date": "2024-11-15T00:00:00Z",
  "rental_date": "2024-11-07T10:35:00Z"
}
```

## 🔧 Key Features

- ✅ 15 sample cars pre-loaded
- ✅ Real-time availability updates
- ✅ Overlap prevention for rentals
- ✅ Automatic cost calculation
- ✅ Car availability management
- ✅ NoSQL scalability
- ✅ No database schema migrations needed

## 📚 Documentation

- **Installation Guide**: [INSTALLATION.md](INSTALLATION.md)
- **Firestore Setup**: [FIRESTORE_SETUP.md](FIRESTORE_SETUP.md)
- **API Documentation**: http://localhost:8000/docs (after starting backend)

## ❓ Troubleshooting

### Firestore Not Found Error
→ You haven't created the Firestore database yet. See Step 1 above.

### Permission Denied
→ Check that credentials.json has the correct permissions (Firestore User/Admin role)

### No Cars Showing
→ Run `python seed_firestore.py` to add sample data

### Backend Won't Start
→ Ensure Firestore is created and credentials.json is in the project root

## 🎯 Next Steps

1. **Create Firestore database** (Step 1 above)
2. **Seed sample data** (`python seed_firestore.py`)
3. **Start both servers** (backend + frontend)
4. **Test the application** (rent a car, cancel rental)
5. **View data in Firestore Console**

## 💡 Production Considerations

Before deploying to production:

1. Update Firestore security rules (currently open for development)
2. Set proper CORS origins in main.py
3. Add authentication/authorization
4. Configure environment variables
5. Enable monitoring and logging
6. Set up backups

## 📞 Support

For issues:
- Check [FIRESTORE_SETUP.md](FIRESTORE_SETUP.md) for detailed Firestore setup
- Review [INSTALLATION.md](INSTALLATION.md) for installation steps
- Check API docs at http://localhost:8000/docs
- View Firestore data in Google Cloud Console
