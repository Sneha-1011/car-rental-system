import os
import json
from google.cloud import firestore
from google.oauth2 import service_account

# Load credentials (looks in parent directory and backend directory)
CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials.json")
if not os.path.exists(CREDENTIALS_PATH):
    # Fallback to backend directory
    CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")

# Initialize Firestore client
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
db = firestore.Client(credentials=credentials, project=credentials.project_id)

# Collection names
CARS_COLLECTION = "cars"
RENTALS_COLLECTION = "rentals"

def get_db():
    """Return Firestore client instance"""
    return db
