from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    print("Starting Car Rental System API...")
    print("Using Google Firestore as database...")
    yield
    # Shutdown: Clean up resources
    print("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title="Car Rental System API",
    description="""
    A comprehensive Car Rental System API that allows you to:
    
    * **Manage Cars**: Add, view, and update car inventory
    * **Rent Cars**: Book cars for specific periods with validation
    * **Manage Rentals**: View and cancel rental bookings
    
    ## Business Rules
    
    - Cars cannot be rented for overlapping dates
    - Rentals must have valid date ranges (end date after start date)
    - Canceling a rental makes the car available again
    - Only available cars can be rented
    
    ## Features
    
    - Complete CRUD operations for cars and rentals
    - Automatic availability management
    - Date overlap validation
    - Cost calculation based on rental duration
    - Google Firestore for scalable NoSQL storage
    - Real-time data synchronization
    """,
    version="1.0.0",
    contact={
        "name": "Car Rental System",
        "email": "support@carrental.com",
    },
    license_info={
        "name": "MIT License",
    },
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, tags=["Car Rental"])


# Root endpoint
@app.get("/", tags=["Health Check"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to Car Rental System API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


# Health check endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }


# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "error": str(exc)
        },
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
