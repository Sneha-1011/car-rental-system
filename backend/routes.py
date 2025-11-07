from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, timezone
import schemas
from db import get_db, CARS_COLLECTION, RENTALS_COLLECTION

router = APIRouter()
db = get_db()


def check_car_availability(car_id: str, start_date: datetime, end_date: datetime, exclude_rental_id: str = None):
    """Check if a car is available for the specified date range"""
    rentals_ref = db.collection(RENTALS_COLLECTION).where("car_id", "==", car_id)
    
    if exclude_rental_id:
        rentals_ref = rentals_ref.where("id", "!=", exclude_rental_id)
    
    rentals = rentals_ref.stream()
    
    for rental_doc in rentals:
        rental = rental_doc.to_dict()
        rental_start = rental['start_date']
        rental_end = rental['end_date']
        
        if start_date < rental_end and end_date > rental_start:
            return False
    
    return True


def calculate_rental_cost(daily_rate: float, start_date: datetime, end_date: datetime) -> float:
    """Calculate total rental cost based on daily rate and rental period"""
    rental_days = (end_date - start_date).days
    if rental_days == 0:
        rental_days = 1
    return daily_rate * rental_days


@router.post("/cars/", response_model=schemas.Car, status_code=status.HTTP_201_CREATED)
def add_car(car: schemas.CarCreate):
    """Add a new car to the rental system"""
    car_data = car.dict()
    car_data['created_at'] = datetime.now(timezone.utc)
    
    doc_ref = db.collection(CARS_COLLECTION).add(car_data)
    car_id = doc_ref[1].id
    
    # Store the document ID in the car for easy lookups
    db.collection(CARS_COLLECTION).document(car_id).update({"doc_id": car_id})
    
    car_data['id'] = abs(hash(car_id)) % (10 ** 10)
    return schemas.Car(**car_data)


@router.get("/cars/", response_model=List[schemas.Car])
def get_all_cars(skip: int = 0, limit: int = 100, available_only: bool = False):
    """Retrieve all cars in the system"""
    query = db.collection(CARS_COLLECTION)
    
    if available_only:
        query = query.where("available", "==", True)
    
    cars_docs = query.limit(limit + skip).stream()
    cars = []
    
    for idx, doc in enumerate(cars_docs):
        if idx < skip:
            continue
        car_data = doc.to_dict()
        
        # Get numeric ID from stored doc_id or calculate from document ID
        if 'doc_id' in car_data:
            car_data['id'] = abs(hash(car_data['doc_id'])) % (10 ** 10)
        else:
            car_data['id'] = abs(hash(doc.id)) % (10 ** 10)
        
        cars.append(schemas.Car(**car_data))
    
    return cars


@router.get("/cars/{car_id}", response_model=schemas.Car)
def get_car(car_id: int):
    """Retrieve details of a specific car by its ID"""
    cars_ref = db.collection(CARS_COLLECTION)
    
    for doc in cars_ref.stream():
        car_data = doc.to_dict()
        
        # Get numeric ID from stored doc_id or calculate from document ID
        if 'doc_id' in car_data:
            doc_numeric_id = abs(hash(car_data['doc_id'])) % (10 ** 10)
        else:
            doc_numeric_id = abs(hash(doc.id)) % (10 ** 10)
        
        if doc_numeric_id == car_id:
            car_data['id'] = car_id
            return schemas.Car(**car_data)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Car with id {car_id} not found"
    )


@router.post("/cars/{car_id}/rent", response_model=schemas.RentalWithTotal, status_code=status.HTTP_201_CREATED)
def rent_car(car_id: int, rental: schemas.RentalBase):
    """Rent a car for a specified period"""
    car_doc_id = None
    car_data = None
    
    for doc in db.collection(CARS_COLLECTION).stream():
        doc_data = doc.to_dict()
        
        # Get numeric ID from stored doc_id or calculate from document ID
        if 'doc_id' in doc_data:
            doc_numeric_id = abs(hash(doc_data['doc_id'])) % (10 ** 10)
        else:
            doc_numeric_id = abs(hash(doc.id)) % (10 ** 10)
        
        if doc_numeric_id == car_id:
            car_doc_id = doc.id
            car_data = doc_data
            break
    
    if not car_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    
    now = datetime.now(timezone.utc)
    start_compare = rental.start_date
    if start_compare.tzinfo is None:
        start_compare = start_compare.replace(tzinfo=timezone.utc)
    
    if start_compare < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be in the past"
        )
    
    if not check_car_availability(car_doc_id, rental.start_date, rental.end_date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Car is not available for the specified dates. Please choose different dates."
        )
    
    rental_data = {
        "car_id": car_doc_id,
        "user_name": rental.user_name,
        "start_date": rental.start_date,
        "end_date": rental.end_date,
        "rental_date": datetime.now(timezone.utc)
    }
    
    doc_ref = db.collection(RENTALS_COLLECTION).add(rental_data)
    rental_doc_id = doc_ref[1].id
    
    # Store the document ID in the rental for easy lookups
    db.collection(RENTALS_COLLECTION).document(rental_doc_id).update({"doc_id": rental_doc_id})
    
    # Check active rentals (filter by car_id first, then filter by date in Python to avoid index requirement)
    all_rentals = db.collection(RENTALS_COLLECTION).where("car_id", "==", car_doc_id).stream()
    active_rentals = [r for r in all_rentals if r.to_dict().get('end_date', datetime.min.replace(tzinfo=timezone.utc)) > now]
    
    if len(active_rentals) > 0:
        db.collection(CARS_COLLECTION).document(car_doc_id).update({"available": False})
    
    total_cost = calculate_rental_cost(car_data['daily_rate'], rental.start_date, rental.end_date)
    
    # Use document ID as the numeric ID for consistency
    rental_data['id'] = abs(hash(rental_doc_id)) % (10 ** 10)  # Use abs() for positive numbers
    rental_data['doc_id'] = rental_doc_id
    rental_data['car_id'] = car_id
    rental_data['total_cost'] = total_cost
    
    return schemas.RentalWithTotal(**rental_data)


@router.delete("/rentals/{rental_id}", response_model=schemas.Message)
def cancel_rental(rental_id: int):
    """Cancel an active rental"""
    rental_doc_id = None
    rental_data = None
    
    # Search by the numeric ID hash
    for doc in db.collection(RENTALS_COLLECTION).stream():
        doc_data = doc.to_dict()
        # Check if this document has a stored doc_id or calculate hash
        if 'doc_id' in doc_data:
            doc_numeric_id = abs(hash(doc_data['doc_id'])) % (10 ** 10)
        else:
            doc_numeric_id = abs(hash(doc.id)) % (10 ** 10)
        
        if doc_numeric_id == rental_id:
            rental_doc_id = doc.id
            rental_data = doc_data
            break
    
    if not rental_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rental with id {rental_id} not found"
        )
    
    car_doc_id = rental_data['car_id']
    
    db.collection(RENTALS_COLLECTION).document(rental_doc_id).delete()
    
    # Check remaining rentals (filter by car_id first, then filter by date in Python to avoid index requirement)
    now = datetime.now(timezone.utc)
    all_rentals = db.collection(RENTALS_COLLECTION).where("car_id", "==", car_doc_id).stream()
    remaining_rentals = [r for r in all_rentals if r.to_dict().get('end_date', datetime.min.replace(tzinfo=timezone.utc)) > now]
    
    if len(remaining_rentals) == 0:
        db.collection(CARS_COLLECTION).document(car_doc_id).update({"available": True})
    
    return {"message": f"Rental {rental_id} has been successfully cancelled"}


@router.get("/rentals/", response_model=List[schemas.Rental])
def get_all_rentals(skip: int = 0, limit: int = 100):
    """Retrieve all rentals in the system"""
    rentals_docs = db.collection(RENTALS_COLLECTION).limit(limit + skip).stream()
    rentals = []
    
    for idx, doc in enumerate(rentals_docs):
        if idx < skip:
            continue
        rental_data = doc.to_dict()
        
        # Get numeric ID from stored doc_id or calculate from document ID
        if 'doc_id' in rental_data:
            rental_data['id'] = abs(hash(rental_data['doc_id'])) % (10 ** 10)
        else:
            rental_data['id'] = abs(hash(doc.id)) % (10 ** 10)
        
        car_doc_id = rental_data['car_id']
        for car_doc in db.collection(CARS_COLLECTION).stream():
            if car_doc.id == car_doc_id:
                rental_data['car_id'] = abs(hash(car_doc.id)) % (10 ** 10)
                break
        
        rentals.append(schemas.Rental(**rental_data))
    
    return rentals


@router.get("/rentals/{rental_id}", response_model=schemas.Rental)
def get_rental(rental_id: int):
    """Retrieve details of a specific rental by its ID"""
    for doc in db.collection(RENTALS_COLLECTION).stream():
        doc_data = doc.to_dict()
        
        # Get numeric ID from stored doc_id or calculate from document ID
        if 'doc_id' in doc_data:
            doc_numeric_id = abs(hash(doc_data['doc_id'])) % (10 ** 10)
        else:
            doc_numeric_id = abs(hash(doc.id)) % (10 ** 10)
        
        if doc_numeric_id == rental_id:
            rental_data = doc_data
            rental_data['id'] = rental_id
            
            car_doc_id = rental_data['car_id']
            for car_doc in db.collection(CARS_COLLECTION).stream():
                if car_doc.id == car_doc_id:
                    rental_data['car_id'] = abs(hash(car_doc.id)) % (10 ** 10)
                    break
            
            return schemas.Rental(**rental_data)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Rental with id {rental_id} not found"
    )
