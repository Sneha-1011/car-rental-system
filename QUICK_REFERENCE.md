# 🚀 Quick Reference Card - Car Rental System

## 📋 Essential Commands

### Initial Setup (One-time)
```powershell
.\setup.ps1
```

### Run Application
```powershell
.\run.ps1
```

### Run All Tests
```powershell
.\test_all.ps1
```

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation (Swagger) | http://localhost:8000/docs |
| API Documentation (ReDoc) | http://localhost:8000/redoc |
| OpenAPI Spec | http://localhost:8000/openapi.json |

## 🧪 Testing Commands

### Backend Tests
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest test_main.py -v
```

### Backend Tests with Coverage
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest test_main.py -v --cov=. --cov-report=html
```

### View Coverage Report
```powershell
cd backend\htmlcov
Start-Process index.html
```

## 🔧 Manual Setup Commands

### Backend Setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend Setup
```powershell
cd frontend
npm install
```

### Database Initialization
```powershell
cd backend
python -c "import sqlite3; conn = sqlite3.connect('car_rental.db'); conn.executescript(open('seed_data.sql').read()); conn.commit(); conn.close()"
```

## 🎯 SDK Generation

### Install OpenAPI Generator
```powershell
npm install -g @openapitools/openapi-generator-cli
```

### Generate Python SDK
```powershell
# Start backend first!
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o car_rental_sdk --package-name car_rental_client
```

### Install SDK
```powershell
cd car_rental_sdk
pip install -e .
```

### Test SDK
```powershell
python ..\test_sdk.py
```

## 🔍 Useful Commands

### Check Running Processes
```powershell
# Check if backend is running
netstat -ano | findstr :8000

# Check if frontend is running
netstat -ano | findstr :3000
```

### Stop Services
```powershell
# Kill process on port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# Kill process on port 3000
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process -Force
```

### Backend Only
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

### Frontend Only
```powershell
cd frontend
npm start
```

## 🗄️ Database Commands

### View Database (SQLite)
```powershell
sqlite3 backend\car_rental.db
```

### Common SQLite Queries
```sql
-- View all tables
.tables

-- View all cars
SELECT * FROM cars;

-- View all rentals
SELECT * FROM rentals;

-- View available cars
SELECT * FROM cars WHERE available = 1;

-- Exit SQLite
.quit
```

### Reset Database
```powershell
cd backend
Remove-Item car_rental.db -ErrorAction SilentlyContinue
python -c "import sqlite3; conn = sqlite3.connect('car_rental.db'); conn.executescript(open('seed_data.sql').read()); conn.commit(); conn.close()"
```

## 📦 Build Commands

### Frontend Production Build
```powershell
cd frontend
npm run build
```

### Serve Production Build
```powershell
cd frontend\build
python -m http.server 3000
```

## 🐛 Debugging

### Enable Backend Debug Mode
```powershell
cd backend
.\venv\Scripts\Activate.ps1
$env:DEBUG = "true"
python main.py
```

### View Backend Logs
Backend logs appear in the console where you ran `python main.py`

### Clear npm Cache
```powershell
cd frontend
npm cache clean --force
Remove-Item node_modules -Recurse -Force
npm install
```

### Clear pip Cache
```powershell
pip cache purge
```

## 📊 Project Structure Commands

### View File Tree
```powershell
tree /F /A
```

### Count Lines of Code
```powershell
# Backend Python files
(Get-ChildItem backend\*.py -Recurse | Get-Content).Count

# Frontend JavaScript files
(Get-ChildItem frontend\src\*.js -Recurse | Get-Content).Count
```

## 🔐 Environment Variables

### Set Google Cloud SQL Mode
```powershell
$env:USE_CLOUD_SQL = "true"
```

### Set SQLite Mode (Default)
```powershell
$env:USE_CLOUD_SQL = "false"
```

## 📖 Documentation

### Main Documentation
- `README.md` - Complete setup and usage guide
- `SDK_GENERATION.md` - SDK generation and usage
- `DEPLOYMENT.md` - Production deployment guide
- `PROJECT_SUMMARY.md` - Project overview and deliverables
- `QUICK_REFERENCE.md` - This file

### View Documentation
```powershell
# Open in default browser
Start-Process README.md
```

## 🚨 Common Issues & Solutions

### Issue: "Python not found"
```powershell
# Install Python 3.8+ from python.org
# Add to PATH during installation
```

### Issue: "Node not found"
```powershell
# Install Node.js 14+ from nodejs.org
```

### Issue: Port already in use
```powershell
# Find and kill process
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### Issue: Cannot activate venv
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Module not found
```powershell
# Activate venv and reinstall
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📞 Getting Help

### Check System Status
```powershell
.\test_all.ps1
```

### View API Documentation
Open http://localhost:8000/docs in browser (after starting backend)

### Check Backend Health
```powershell
curl http://localhost:8000/health
```

### Test API Endpoint
```powershell
curl http://localhost:8000/cars/
```

---

**💡 Tip**: Keep this file open in a text editor for quick reference!

**🔖 Bookmark**: http://localhost:8000/docs for interactive API testing
