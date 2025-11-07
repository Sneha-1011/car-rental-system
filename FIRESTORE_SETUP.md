# Firestore Setup Instructions

## Error: Firestore Database Not Created

The error indicates that Firestore hasn't been set up in your Google Cloud project yet.

## Setup Steps

### Option 1: Using Google Cloud Console (Recommended)

1. **Visit the Firestore Setup Page**
   
   Open this URL in your browser:
   ```
   https://console.cloud.google.com/datastore/setup?project=skill-sync-ai-472908
   ```

2. **Select Firestore Mode**
   
   - Choose **"Firestore Native Mode"** (recommended for new applications)
   - Do NOT choose "Datastore Mode"

3. **Select a Location**
   
   - Choose a location close to your users (e.g., `us-central1`, `us-east1`, `europe-west1`)
   - **Important**: This cannot be changed later!

4. **Click "Create Database"**
   
   - Wait for the database to be created (usually takes 1-2 minutes)

5. **Return to Terminal and Run Seed Script**
   ```cmd
   cd "c:\Users\HP\Downloads\Car Rental\backend"
   venv\Scripts\activate
   python seed_firestore.py
   ```

### Option 2: Using gcloud CLI (Alternative)

If you have the Google Cloud SDK installed:

```cmd
gcloud firestore databases create --location=us-central1 --project=skill-sync-ai-472908
```

Then run the seed script:
```cmd
python seed_firestore.py
```

## After Setup

Once Firestore is created:

1. **Seed the database**:
   ```cmd
   python seed_firestore.py
   ```

2. **Start the backend**:
   ```cmd
   uvicorn main:app --reload
   ```

3. **Verify in Firestore Console**:
   - Go to: https://console.cloud.google.com/firestore/databases/-default-/data/panel?project=skill-sync-ai-472908
   - You should see the `cars` collection with 15 documents

## Firestore Security Rules (Optional)

For development, you can start with these permissive rules (update for production):

1. Go to: https://console.cloud.google.com/firestore/databases/-default-/rules?project=skill-sync-ai-472908

2. Set rules to:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;  // Change this for production!
    }
  }
}
```

3. Click "Publish"

**Warning**: These rules allow anyone to read/write. For production, implement proper authentication and authorization.

## Next Steps

After creating the Firestore database:

1. Run `python seed_firestore.py` to add sample cars
2. Start the backend: `uvicorn main:app --reload`
3. Start the frontend: `npm start` (in frontend directory)
4. Access the app at http://localhost:3000

## Troubleshooting

### Permission Denied
- Ensure your `credentials.json` has the "Cloud Datastore User" or "Firebase Admin" role
- Update IAM permissions in Google Cloud Console

### Wrong Project
- Verify project ID in `credentials.json` matches: `skill-sync-ai-472908`

### Location Errors
- Choose a location from: https://cloud.google.com/firestore/docs/locations
