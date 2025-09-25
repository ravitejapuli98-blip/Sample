"""
API v1 router configuration
"""

from fastapi import APIRouter
from app.api.v1.endpoints import cities, policies, simulations, predictions, data

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(cities.router, prefix="/cities", tags=["cities"])
api_router.include_router(policies.router, prefix="/policies", tags=["policies"])
api_router.include_router(simulations.router, prefix="/simulations", tags=["simulations"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(data.router, prefix="/data", tags=["data"])
