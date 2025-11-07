# Python SDK Generation Guide

This guide explains how to generate and use the Python SDK for the Car Rental System API using OpenAPI Generator CLI.

## Prerequisites

1. **Install OpenAPI Generator CLI**:
   ```bash
   npm install -g @openapitools/openapi-generator-cli
   ```

2. **Ensure the Backend Server is Running**:
   The backend must be running to access the OpenAPI specification.
   ```bash
   cd backend
   .\venv\Scripts\Activate.ps1
   python main.py
   ```

## Generate the SDK

Once the backend is running, generate the Python SDK:

```bash
# From the root directory of the project
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o car_rental_sdk --package-name car_rental_client
```

### Generator Options Explained:
- `-i http://localhost:8000/openapi.json`: Input OpenAPI specification URL
- `-g python`: Generate Python SDK
- `-o car_rental_sdk`: Output directory for the generated SDK
- `--package-name car_rental_client`: Name of the Python package

## Install the Generated SDK

After generation, install the SDK:

```bash
cd car_rental_sdk
pip install -e .
```

## Using the SDK

### Example 1: List All Cars

```python
from car_rental_client import ApiClient, Configuration
from car_rental_client.api import default_api

# Configure the API client
configuration = Configuration(
    host="http://localhost:8000"
)

with ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    
    try:
        # Get all cars
        cars = api_instance.get_all_cars_cars_get()
        print("Available Cars:")
        for car in cars:
            print(f"- {car.make} {car.model} ({car.year}): ${car.daily_rate}/day")
    except Exception as e:
        print(f"Error: {e}")
```

### Example 2: Add a New Car

```python
from car_rental_client import ApiClient, Configuration
from car_rental_client.api import default_api
from car_rental_client.model.car_create import CarCreate

configuration = Configuration(host="http://localhost:8000")

with ApiClient(configuration) as api_client:
    api_instance = default_api.DefaultApi(api_client)
    
    # Create a new car
    new_car = CarCreate(
        make="Tesla",
        model="Model S",
        year=2024,
        daily_rate=150.0,
        available=True
    )
    
    try:
        result = api_instance.add_car_cars_post(car_create=new_car)
        print(f"Car added successfully! ID: {result.id}")
    except Exception as e:
        print(f"Error: {e}")
```

### Example 3: Rent a Car

```python
from car_rental_client import ApiClient, Configuration
from car_rental_client.api import default_api
from car_rental_client.model.rental_base import RentalBase
from datetime import datetime, timedelta

configuration = Configuration(host="http://localhost:8000")

with ApiClient(configuration) as api_client:
    api_instance = default_api.DefaultApi(api_client)
    
    # Rent a car
    car_id = 1  # Replace with actual car ID
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=5)
    
    rental_data = RentalBase(
        user_name="John Doe",
        start_date=start_date,
        end_date=end_date
    )
    
    try:
        result = api_instance.rent_car_cars_car_id_rent_post(
            car_id=car_id,
            rental_base=rental_data
        )
        print(f"Rental successful! Rental ID: {result.id}")
        print(f"Total Cost: ${result.total_cost}")
    except Exception as e:
        print(f"Error: {e}")
```

### Example 4: Cancel a Rental

```python
from car_rental_client import ApiClient, Configuration
from car_rental_client.api import default_api

configuration = Configuration(host="http://localhost:8000")

with ApiClient(configuration) as api_client:
    api_instance = default_api.DefaultApi(api_client)
    
    rental_id = 1  # Replace with actual rental ID
    
    try:
        result = api_instance.cancel_rental_rentals_rental_id_delete(rental_id=rental_id)
        print(result.message)
    except Exception as e:
        print(f"Error: {e}")
```

## Complete SDK Test Script

Create a file named `test_sdk.py` in the `car_rental_sdk` directory:

```python
"""
Test script for the Car Rental System SDK
"""
from car_rental_client import ApiClient, Configuration
from car_rental_client.api import default_api
from car_rental_client.model.car_create import CarCreate
from car_rental_client.model.rental_base import RentalBase
from datetime import datetime, timedelta

def test_sdk():
    # Configure the API client
    configuration = Configuration(
        host="http://localhost:8000"
    )
    
    with ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        
        print("=" * 50)
        print("Car Rental System SDK Test")
        print("=" * 50)
        
        # Test 1: List all cars
        print("\n1. Listing all available cars...")
        try:
            cars = api_instance.get_all_cars_cars_get(available_only=True)
            print(f"Found {len(cars)} available cars:")
            for car in cars:
                print(f"  - [{car.id}] {car.make} {car.model} ({car.year}): ${car.daily_rate}/day")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 2: Add a new car
        print("\n2. Adding a new car...")
        try:
            new_car = CarCreate(
                make="Porsche",
                model="911 Carrera",
                year=2024,
                daily_rate=250.0,
                available=True
            )
            result = api_instance.add_car_cars_post(car_create=new_car)
            print(f"✓ Car added successfully! ID: {result.id}")
            new_car_id = result.id
        except Exception as e:
            print(f"Error: {e}")
            new_car_id = None
        
        # Test 3: Get specific car
        if new_car_id:
            print(f"\n3. Getting details for car ID {new_car_id}...")
            try:
                car = api_instance.get_car_cars_car_id_get(car_id=new_car_id)
                print(f"✓ {car.make} {car.model} - ${car.daily_rate}/day")
            except Exception as e:
                print(f"Error: {e}")
        
        # Test 4: Rent a car
        if cars and len(cars) > 0:
            print(f"\n4. Renting car ID {cars[0].id}...")
            try:
                start_date = datetime.now() + timedelta(days=2)
                end_date = start_date + timedelta(days=5)
                
                rental_data = RentalBase(
                    user_name="SDK Test User",
                    start_date=start_date,
                    end_date=end_date
                )
                
                rental = api_instance.rent_car_cars_car_id_rent_post(
                    car_id=cars[0].id,
                    rental_base=rental_data
                )
                print(f"✓ Rental successful! Rental ID: {rental.id}")
                print(f"  Total Cost: ${rental.total_cost}")
                test_rental_id = rental.id
            except Exception as e:
                print(f"Error: {e}")
                test_rental_id = None
        
        # Test 5: Cancel rental
        if test_rental_id:
            print(f"\n5. Canceling rental ID {test_rental_id}...")
            try:
                result = api_instance.cancel_rental_rentals_rental_id_delete(
                    rental_id=test_rental_id
                )
                print(f"✓ {result.message}")
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n" + "=" * 50)
        print("SDK Test Complete!")
        print("=" * 50)

if __name__ == "__main__":
    test_sdk()
```

## Running the Test Script

```bash
cd car_rental_sdk
python test_sdk.py
```

## Troubleshooting

### Issue: Cannot connect to API
**Solution**: Ensure the backend server is running on `http://localhost:8000`

### Issue: Import errors
**Solution**: Make sure you've installed the SDK with `pip install -e .`

### Issue: Authentication errors
**Solution**: This API doesn't require authentication by default. Check your configuration.

## SDK Documentation

After generation, you can find detailed SDK documentation in:
- `car_rental_sdk/README.md`
- `car_rental_sdk/docs/`

## Regenerating the SDK

If you make changes to the API, regenerate the SDK:

1. Stop the old SDK server if running
2. Delete the old SDK directory: `rm -r car_rental_sdk`
3. Restart the backend server
4. Run the generation command again

## Advanced Configuration

### Custom API Endpoint

```python
configuration = Configuration(
    host="https://your-production-api.com"
)
```

### Timeout Configuration

```python
configuration = Configuration(
    host="http://localhost:8000"
)
configuration.timeout = 30  # 30 seconds
```

### Debugging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
```
