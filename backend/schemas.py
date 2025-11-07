from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

# Car Schemas
class CarBase(BaseModel):
    """Base schema for Car"""
    make: str = Field(..., min_length=1, max_length=100, description="Car manufacturer")
    model: str = Field(..., min_length=1, max_length=100, description="Car model name")
    year: int = Field(..., ge=1900, le=2100, description="Manufacturing year")
    daily_rate: float = Field(..., gt=0, description="Daily rental rate in dollars")

class CarCreate(CarBase):
    """Schema for creating a new car"""
    available: Optional[bool] = True

class CarUpdate(BaseModel):
    """Schema for updating car details"""
    make: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    daily_rate: Optional[float] = Field(None, gt=0)
    available: Optional[bool] = None

class Car(CarBase):
    """Schema for returning car data"""
    id: int
    available: bool

    class Config:
        from_attributes = True


# Rental Schemas
class RentalBase(BaseModel):
    """Base schema for Rental"""
    user_name: str = Field(..., min_length=1, max_length=200, description="Name of the person renting")
    start_date: datetime = Field(..., description="Rental start date and time")
    end_date: datetime = Field(..., description="Rental end date and time")

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class RentalCreate(RentalBase):
    """Schema for creating a new rental"""
    car_id: int = Field(..., description="ID of the car to rent")

class Rental(RentalBase):
    """Schema for returning rental data"""
    id: int
    car_id: int
    rental_date: datetime
    car: Optional[Car] = None

    class Config:
        from_attributes = True


# Response Schemas
class Message(BaseModel):
    """Generic message response schema"""
    message: str

class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str

class RentalWithTotal(Rental):
    """Rental schema with calculated total cost"""
    total_cost: float = Field(..., description="Total cost of the rental")
