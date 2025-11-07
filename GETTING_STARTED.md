# 🎬 Getting Started - Car Rental System

Welcome! This guide will get you up and running in **5 minutes**.

---

## 📋 Before You Begin

Make sure you have:
- ✅ **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- ✅ **Node.js 14+** installed ([Download here](https://nodejs.org/))
- ✅ **PowerShell** (comes with Windows)

**Check your installations:**
```powershell
python --version    # Should show Python 3.8 or higher
node --version      # Should show v14 or higher
npm --version       # Should show 6 or higher
```

---

## 🚀 Installation (5 Steps)

### Step 1: Navigate to Project Directory
```powershell
cd "C:\Users\HP\Downloads\Car Rental"
```

### Step 2: Run Setup Script
```powershell
.\setup.ps1
```

**What this does:**
- ✅ Creates Python virtual environment
- ✅ Installs backend dependencies
- ✅ Installs frontend dependencies  
- ✅ Initializes database with sample data

**Expected time:** 2-3 minutes

### Step 3: Wait for Setup to Complete
You'll see progress messages. Wait for:
```
✓ All tests passed! System is ready.
```

### Step 4: Start the Application
```powershell
.\run.ps1
```

**What this does:**
- 🖥️ Starts Backend Server (port 8000)
- 🌐 Starts Frontend Server (port 3000)
- Opens in separate windows

### Step 5: Access the Application
The frontend will automatically open in your browser, or visit:

🌐 **Frontend**: http://localhost:3000
📚 **API Docs**: http://localhost:8000/docs

---

## 🎯 First Steps in the Application

### Browse Cars
1. Open http://localhost:3000
2. See list of available cars
3. Toggle "Show available only" to filter
4. Click **🔄 Refresh** to update

### Rent a Car
1. Click **"Rent This Car"** on any available car
2. Fill in your name
3. Select start and end dates
4. See estimated cost
5. Click **"Confirm Rental"**
6. You'll receive a Rental ID - save it!

### Cancel a Rental
1. Click **"Cancel Rental"** tab
2. Enter your Rental ID
3. Click **"Cancel Rental"**
4. The car becomes available again

---

## 📚 Explore the API

Visit **http://localhost:8000/docs** for interactive API documentation.

### Try These Examples:

**1. View All Cars:**
```bash
curl http://localhost:8000/cars/
```

**2. Get a Specific Car:**
```bash
curl http://localhost:8000/cars/1
```

**3. Rent a Car:**
```bash
curl -X POST http://localhost:8000/cars/1/rent \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Your Name",
    "start_date": "2025-11-10T10:00:00",
    "end_date": "2025-11-15T10:00:00"
  }'
```

**4. Cancel a Rental:**
```bash
curl -X DELETE http://localhost:8000/rentals/1
```

---

## 🧪 Run Tests

Verify everything is working:

```powershell
.\test_all.ps1
```

Or run backend tests specifically:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest test_main.py -v
```

**Expected output:**
```
✓ All tests passed! System is ready.
```

---

## 📦 Generate Python SDK (Optional)

Want to integrate the API into your Python projects?

### 1. Install OpenAPI Generator
```powershell
npm install -g @openapitools/openapi-generator-cli
```

### 2. Generate SDK (with backend running)
```powershell
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o car_rental_sdk --package-name car_rental_client
```

### 3. Install SDK
```powershell
cd car_rental_sdk
pip install -e .
```

### 4. Test SDK
```powershell
cd ..
python test_sdk.py
```

**For detailed SDK usage**, see [SDK_GENERATION.md](SDK_GENERATION.md)

---

## 🗂️ Project Structure Overview

```
Car Rental/
├── 📄 Documentation
│   ├── INDEX.md              ← Start here for navigation
│   ├── README.md             ← Complete documentation
│   ├── QUICK_REFERENCE.md    ← Command cheat sheet
│   └── API_EXAMPLES.md       ← API usage examples
│
├── 🔧 Scripts
│   ├── setup.ps1             ← Run once to setup
│   ├── run.ps1               ← Run to start app
│   └── test_all.ps1          ← Run to test
│
├── 🖥️ backend/              ← FastAPI backend
└── 🌐 frontend/             ← React frontend
```

---

## 🎓 Learning Path

### Beginner (Just Want to Use It)
1. ✅ Complete installation steps above
2. 📖 Read this guide
3. 🎯 Use the web application
4. 📚 Explore API docs

### Intermediate (Want to Understand It)
1. 📖 Read [README.md](README.md)
2. 📊 Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. 💻 Study the code in `backend/` and `frontend/`
4. 🧪 Run and study the tests

### Advanced (Want to Extend It)
1. 📖 Read [DEPLOYMENT.md](DEPLOYMENT.md)
2. 🔧 Modify and test locally
3. 🐳 Deploy to production
4. 🤝 Contribute improvements

---

## 📖 Quick Command Reference

| Action | Command |
|--------|---------|
| Setup | `.\setup.ps1` |
| Run | `.\run.ps1` |
| Test | `.\test_all.ps1` |
| Backend only | `cd backend && .\venv\Scripts\Activate.ps1 && python main.py` |
| Frontend only | `cd frontend && npm start` |
| Generate SDK | `openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o car_rental_sdk` |

**Full command reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 🚨 Troubleshooting

### ❌ "Python not found"
**Solution:** Install Python from https://python.org and add to PATH

### ❌ "Node not found"  
**Solution:** Install Node.js from https://nodejs.org

### ❌ "Port 8000 already in use"
**Solution:**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### ❌ "Cannot activate virtual environment"
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ Tests fail
**Solution:** Run setup again:
```powershell
.\setup.ps1
```

**More troubleshooting**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#-troubleshooting)

---

## 🎯 What's Included

✅ **Complete Backend** - FastAPI with 8 endpoints  
✅ **Modern Frontend** - React with 3 main components  
✅ **Database** - SQLite (local) + PostgreSQL (cloud) support  
✅ **Tests** - 18+ unit tests with pytest  
✅ **Documentation** - 6 comprehensive guides  
✅ **Automation** - Setup and run scripts  
✅ **SDK Support** - OpenAPI-based SDK generation  
✅ **Cloud Ready** - Google Cloud SQL integration  

---

## 📞 Need Help?

### Documentation
1. **[INDEX.md](INDEX.md)** - Navigation hub
2. **[README.md](README.md)** - Complete guide
3. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Commands
4. **[API_EXAMPLES.md](API_EXAMPLES.md)** - API usage

### Interactive Help
- 📚 API Docs: http://localhost:8000/docs
- 🔍 Health Check: http://localhost:8000/health

### Run Diagnostics
```powershell
.\test_all.ps1
```

---

## 🎉 Success!

If you've made it here, you should have:

✅ Application running  
✅ Frontend accessible at http://localhost:3000  
✅ Backend API at http://localhost:8000  
✅ Tests passing  

**Next Steps:**
- 🎨 Explore the frontend
- 📚 Try the API at http://localhost:8000/docs
- 🧪 Run tests with `.\test_all.ps1`
- 📖 Read more in [README.md](README.md)

---

## 🌟 Key Features to Try

1. **Browse Cars** - View all available vehicles
2. **Filter Cars** - Toggle "available only" filter
3. **Rent a Car** - Book a car for specific dates
4. **Cost Estimation** - See price calculation in real-time
5. **Cancel Rental** - Free up cars by canceling bookings
6. **API Exploration** - Try endpoints at `/docs`

---

## 📊 Sample Data

The system comes with **15 sample cars**:
- Toyota Camry ($45/day)
- Honda Civic ($40/day)
- Ford Mustang ($75/day)
- Tesla Model 3 ($95/day)
- BMW X5 ($120/day)
- And 10 more!

---

## 🔐 Google Cloud Integration

The system supports Google Cloud SQL for production.

**Currently configured for:**
- 🔧 **Local**: SQLite (default, no setup needed)
- ☁️ **Production**: Google Cloud SQL PostgreSQL

**To enable Cloud SQL:**
1. Update `backend/db.py` with your instance details
2. Set `$env:USE_CLOUD_SQL = "true"`
3. Ensure `credentials.json` is present

**More details**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 💡 Tips

- 💾 **Save Rental IDs** - You'll need them to cancel
- 🔄 **Refresh Often** - Click refresh to see latest data
- 📅 **Check Dates** - System prevents double-booking
- 📖 **Read Docs** - Visit `/docs` for API details
- 🧪 **Run Tests** - Use `.\test_all.ps1` regularly

---

**🚀 You're all set! Enjoy using the Car Rental System!**

**Questions?** Check [INDEX.md](INDEX.md) for complete documentation navigation.
