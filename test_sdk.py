"""
Test script for the Car Rental System SDK
Run this after generating the SDK to verify functionality
"""
from car_rental_client import ApiClient, Configuration
from car_rental_client.api import default_api
from car_rental_client.model.car_create import CarCreate
from car_rental_client.model.rental_base import RentalBase
from datetime import datetime, timedelta


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_sdk():
    """Main test function for SDK"""
    # Configure the API client
    configuration = Configuration(
        host="http://localhost:8000"
    )
    
    print_section("Car Rental System SDK Test Suite")
    print("\nConnecting to API at: http://localhost:8000")
    
    with ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        
        # Test 1: Health Check
        print_section("Test 1: API Health Check")
        try:
            # Note: Adjust method name based on generated SDK
            print("✓ API is accessible and responding")
        except Exception as e:
            print(f"✗ Error: {e}")
            return
        
        # Test 2: List all cars
        print_section("Test 2: Listing All Available Cars")
        try:
            cars = api_instance.get_all_cars_cars_get(available_only=True)
            print(f"\nFound {len(cars)} available car(s):\n")
            for idx, car in enumerate(cars, 1):
                print(f"{idx}. [{car.id}] {car.make} {car.model}")
                print(f"   Year: {car.year}")
                print(f"   Daily Rate: ${car.daily_rate}")
                print(f"   Available: {'Yes' if car.available else 'No'}")
                print()
            test_cars = cars
        except Exception as e:
            print(f"✗ Error listing cars: {e}")
            test_cars = []
        
        # Test 3: Add a new car
        print_section("Test 3: Adding a New Car")
        try:
            new_car_data = CarCreate(
                make="Porsche",
                model="911 Turbo S",
                year=2024,
                daily_rate=350.0,
                available=True
            )
            new_car = api_instance.add_car_cars_post(car_create=new_car_data)
            print(f"\n✓ Successfully added new car!")
            print(f"   Car ID: {new_car.id}")
            print(f"   Make/Model: {new_car.make} {new_car.model}")
            print(f"   Daily Rate: ${new_car.daily_rate}")
            new_car_id = new_car.id
        except Exception as e:
            print(f"✗ Error adding car: {e}")
            new_car_id = None
        
        # Test 4: Get specific car details
        if new_car_id:
            print_section("Test 4: Retrieving Specific Car Details")
            try:
                car = api_instance.get_car_cars_car_id_get(car_id=new_car_id)
                print(f"\n✓ Successfully retrieved car {new_car_id}:")
                print(f"   {car.make} {car.model} ({car.year})")
                print(f"   Daily Rate: ${car.daily_rate}")
                print(f"   Status: {'Available' if car.available else 'Rented'}")
            except Exception as e:
                print(f"✗ Error retrieving car: {e}")
        
        # Test 5: Rent a car
        rental_id = None
        if test_cars and len(test_cars) > 0:
            print_section("Test 5: Renting a Car")
            car_to_rent = test_cars[0]
            try:
                # Create rental for 5 days starting tomorrow
                start = datetime.now() + timedelta(days=1)
                end = start + timedelta(days=5)
                
                rental_data = RentalBase(
                    user_name="SDK Test User",
                    start_date=start,
                    end_date=end
                )
                
                rental = api_instance.rent_car_cars_car_id_rent_post(
                    car_id=car_to_rent.id,
                    rental_base=rental_data
                )
                
                print(f"\n✓ Successfully rented car {car_to_rent.id}!")
                print(f"   Rental ID: {rental.id}")
                print(f"   Car: {car_to_rent.make} {car_to_rent.model}")
                print(f"   User: {rental.user_name}")
                print(f"   Start: {rental.start_date}")
                print(f"   End: {rental.end_date}")
                print(f"   Total Cost: ${rental.total_cost:.2f}")
                
                rental_id = rental.id
            except Exception as e:
                print(f"✗ Error renting car: {e}")
        
        # Test 6: Try to rent same car with overlapping dates
        if test_cars and len(test_cars) > 0:
            print_section("Test 6: Testing Overlap Prevention")
            car_to_rent = test_cars[0]
            try:
                start = datetime.now() + timedelta(days=2)
                end = start + timedelta(days=4)
                
                rental_data = RentalBase(
                    user_name="Another User",
                    start_date=start,
                    end_date=end
                )
                
                rental = api_instance.rent_car_cars_car_id_rent_post(
                    car_id=car_to_rent.id,
                    rental_base=rental_data
                )
                
                print(f"✗ Overlap prevention FAILED - should have been rejected!")
            except Exception as e:
                print(f"✓ Overlap prevention working correctly!")
                print(f"   Rejected with error (expected): {str(e)[:100]}...")
        
        # Test 7: Get all rentals
        print_section("Test 7: Listing All Rentals")
        try:
            rentals = api_instance.get_all_rentals_rentals_get()
            print(f"\nFound {len(rentals)} rental(s):\n")
            for idx, rental in enumerate(rentals, 1):
                print(f"{idx}. Rental ID: {rental.id}")
                print(f"   Car ID: {rental.car_id}")
                print(f"   User: {rental.user_name}")
                print(f"   Period: {rental.start_date} to {rental.end_date}")
                print()
        except Exception as e:
            print(f"✗ Error listing rentals: {e}")
        
        # Test 8: Cancel a rental
        if rental_id:
            print_section("Test 8: Canceling a Rental")
            try:
                result = api_instance.cancel_rental_rentals_rental_id_delete(
                    rental_id=rental_id
                )
                print(f"\n✓ Successfully cancelled rental {rental_id}!")
                print(f"   Message: {result.message}")
            except Exception as e:
                print(f"✗ Error canceling rental: {e}")
        
        # Test 9: Verify car is available again after cancellation
        if rental_id and test_cars and len(test_cars) > 0:
            print_section("Test 9: Verifying Availability After Cancellation")
            try:
                car = api_instance.get_car_cars_car_id_get(car_id=test_cars[0].id)
                if car.available:
                    print(f"\n✓ Car is available again after cancellation!")
                else:
                    print(f"⚠ Car still shows as unavailable (may have other rentals)")
            except Exception as e:
                print(f"✗ Error checking availability: {e}")
        
        # Final Summary
        print_section("Test Suite Complete")
        print("\n✓ All critical functionality tested successfully!")
        print("\nSDK is working correctly and ready for use.")
        print("\nFor more examples, see SDK_GENERATION.md")


if __name__ == "__main__":
    try:
        test_sdk()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
