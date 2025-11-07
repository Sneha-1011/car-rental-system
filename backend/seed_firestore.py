"""
Seed script to populate Firestore with sample car data
"""
from db import db, CARS_COLLECTION
from datetime import datetime, timezone

# Sample car data
sample_cars = [
    {"make": "Toyota", "model": "Camry", "year": 2022, "daily_rate": 45.00, "available": True},
    {"make": "Honda", "model": "Accord", "year": 2023, "daily_rate": 50.00, "available": True},
    {"make": "Ford", "model": "Mustang", "year": 2021, "daily_rate": 75.00, "available": True},
    {"make": "Chevrolet", "model": "Malibu", "year": 2022, "daily_rate": 42.00, "available": True},
    {"make": "BMW", "model": "3 Series", "year": 2023, "daily_rate": 95.00, "available": True},
    {"make": "Mercedes-Benz", "model": "C-Class", "year": 2023, "daily_rate": 100.00, "available": True},
    {"make": "Audi", "model": "A4", "year": 2022, "daily_rate": 90.00, "available": True},
    {"make": "Tesla", "model": "Model 3", "year": 2023, "daily_rate": 110.00, "available": True},
    {"make": "Nissan", "model": "Altima", "year": 2022, "daily_rate": 40.00, "available": True},
    {"make": "Mazda", "model": "CX-5", "year": 2023, "daily_rate": 55.00, "available": True},
    {"make": "Hyundai", "model": "Sonata", "year": 2022, "daily_rate": 38.00, "available": True},
    {"make": "Kia", "model": "Optima", "year": 2021, "daily_rate": 36.00, "available": True},
    {"make": "Volkswagen", "model": "Passat", "year": 2022, "daily_rate": 48.00, "available": True},
    {"make": "Subaru", "model": "Outback", "year": 2023, "daily_rate": 58.00, "available": True},
    {"make": "Jeep", "model": "Grand Cherokee", "year": 2022, "daily_rate": 70.00, "available": True}
]

def seed_data():
    """Add sample cars to Firestore"""
    print("Starting Firestore seeding...")
    
    # Check if cars already exist
    cars_ref = db.collection(CARS_COLLECTION)
    existing_cars = list(cars_ref.limit(1).stream())
    
    if existing_cars:
        print(f"Database already contains data. Skipping seeding.")
        print(f"To reseed, delete the '{CARS_COLLECTION}' collection first.")
        return
    
    # Add sample cars
    added_count = 0
    for car_data in sample_cars:
        car_data['created_at'] = datetime.now(timezone.utc)
        doc_ref = cars_ref.add(car_data)
        added_count += 1
        print(f"Added: {car_data['year']} {car_data['make']} {car_data['model']} (ID: {doc_ref[1].id})")
    
    print(f"\n✅ Successfully added {added_count} cars to Firestore!")
    print(f"Collection: {CARS_COLLECTION}")

if __name__ == "__main__":
    seed_data()
