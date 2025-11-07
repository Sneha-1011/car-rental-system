# Deployment Guide - Car Rental System

This guide covers deploying the Car Rental System to various environments.

## Table of Contents
- [Local Deployment](#local-deployment)
- [Google Cloud Platform](#google-cloud-platform)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)

## Local Deployment

### Prerequisites
- Python 3.8+
- Node.js 14+
- SQLite (included with Python)

### Steps
1. Run setup script: `.\setup.ps1`
2. Run application: `.\run.ps1`
3. Access at http://localhost:3000

## Google Cloud Platform

### 1. Setup Cloud SQL

```bash
# Create Cloud SQL instance
gcloud sql instances create car-rental-db \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=us-central1

# Create database
gcloud sql databases create car_rental --instance=car-rental-db

# Create user
gcloud sql users create rental_user \
    --instance=car-rental-db \
    --password=SECURE_PASSWORD
```

### 2. Configure Backend

Update `backend/db.py`:
```python
INSTANCE_CONNECTION_NAME = "your-project:us-central1:car-rental-db"
DB_USER = "rental_user"
DB_PASS = "SECURE_PASSWORD"
DB_NAME = "car_rental"
```

Set environment variable:
```powershell
$env:USE_CLOUD_SQL = "true"
```

### 3. Deploy to Cloud Run (Backend)

```bash
# Build and deploy
gcloud run deploy car-rental-api \
    --source ./backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --add-cloudsql-instances your-project:us-central1:car-rental-db \
    --set-env-vars USE_CLOUD_SQL=true
```

### 4. Deploy Frontend to Firebase Hosting

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
cd frontend
firebase init hosting

# Build
npm run build

# Deploy
firebase deploy --only hosting
```

### 5. Update Frontend API URL

In `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'https://car-rental-api-xxxxx-uc.a.run.app';
```

## Docker Deployment

### Backend Dockerfile

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - USE_CLOUD_SQL=false
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

Run with:
```bash
docker-compose up
```

## Environment Variables

### Backend (.env)
```env
USE_CLOUD_SQL=true
GOOGLE_CLOUD_PROJECT=your-project-id
INSTANCE_CONNECTION_NAME=your-project:region:instance
DB_USER=rental_user
DB_PASS=secure_password
DB_NAME=car_rental
```

### Frontend (.env)
```env
REACT_APP_API_URL=https://your-backend-url.com
```

## Production Checklist

- [ ] Update all credentials and secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS with specific origins
- [ ] Set up database backups
- [ ] Configure monitoring and logging
- [ ] Set up rate limiting
- [ ] Enable authentication/authorization
- [ ] Configure CDN for frontend
- [ ] Set up CI/CD pipeline
- [ ] Load testing
- [ ] Security audit

## Monitoring

### Google Cloud Monitoring

```bash
# Enable Cloud Monitoring
gcloud services enable monitoring.googleapis.com

# Create uptime check
gcloud monitoring uptime create car-rental-check \
    --display-name="Car Rental API" \
    --resource-type=uptime-url \
    --host=your-api-url.com \
    --path=/health
```

## Scaling

### Horizontal Scaling (Cloud Run)
```bash
gcloud run services update car-rental-api \
    --min-instances=1 \
    --max-instances=10 \
    --concurrency=80
```

### Database Scaling
```bash
# Upgrade instance
gcloud sql instances patch car-rental-db \
    --tier=db-n1-standard-1
```

## Troubleshooting

### Cloud SQL Connection Issues
- Verify service account has Cloud SQL Client role
- Check VPC configuration
- Ensure credentials.json is properly configured

### Frontend Not Connecting
- Verify CORS settings in backend
- Check API_URL environment variable
- Ensure backend is accessible from frontend domain
