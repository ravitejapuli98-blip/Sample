"""
Real Data Integration Endpoints
Integrates with live city data APIs
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any, Optional
import logging
from ...services.air_quality import air_quality_service
from ...services.transportation import transportation_service
from ...services.energy import energy_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Air Quality Endpoints
@router.get("/air-quality/coordinates")
async def get_air_quality_by_coordinates(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get real-time air quality data by coordinates"""
    try:
        data = air_quality_service.get_air_quality_by_coordinates(lat, lon)
        return {
            "success": True,
            "data": data,
            "message": "Air quality data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting air quality by coordinates: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve air quality data")

@router.get("/air-quality/city/{city_name}")
async def get_air_quality_by_city(
    city_name: str,
    country_code: str = Query("US", description="Country code")
):
    """Get real-time air quality data by city name"""
    try:
        data = air_quality_service.get_air_quality_by_city(city_name, country_code)
        return {
            "success": True,
            "data": data,
            "message": f"Air quality data for {city_name} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting air quality for city {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve air quality data")

@router.get("/air-quality/historical")
async def get_historical_air_quality(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    days: int = Query(7, description="Number of days of historical data")
):
    """Get historical air quality data"""
    try:
        data = air_quality_service.get_historical_air_quality(lat, lon, days)
        return {
            "success": True,
            "data": data,
            "message": f"Historical air quality data for {days} days retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting historical air quality: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve historical air quality data")

@router.get("/air-quality/forecast")
async def get_air_quality_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get air quality forecast"""
    try:
        data = air_quality_service.get_air_quality_forecast(lat, lon)
        return {
            "success": True,
            "data": data,
            "message": "Air quality forecast retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting air quality forecast: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve air quality forecast")

# Transportation Endpoints
@router.get("/transportation/traffic")
async def get_traffic_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius: int = Query(5000, description="Radius in meters")
):
    """Get real-time traffic data"""
    try:
        data = transportation_service.get_traffic_data(lat, lon, radius)
        return {
            "success": True,
            "data": data,
            "message": "Traffic data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting traffic data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve traffic data")

@router.get("/transportation/transit/{city_name}")
async def get_public_transit_data(city_name: str):
    """Get public transit data for a city"""
    try:
        data = transportation_service.get_public_transit_data(city_name)
        return {
            "success": True,
            "data": data,
            "message": f"Public transit data for {city_name} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting transit data for {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve transit data")

@router.get("/transportation/bike-share")
async def get_bike_share_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get bike share station data"""
    try:
        data = transportation_service.get_bike_share_data(lat, lon)
        return {
            "success": True,
            "data": data,
            "message": "Bike share data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting bike share data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve bike share data")

@router.get("/transportation/emissions/{city_name}")
async def get_transportation_emissions(city_name: str):
    """Get transportation emissions data for a city"""
    try:
        data = transportation_service.get_transportation_emissions(city_name)
        return {
            "success": True,
            "data": data,
            "message": f"Transportation emissions data for {city_name} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting emissions data for {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve emissions data")

# Energy Endpoints
@router.get("/energy/consumption/{city_name}")
async def get_energy_consumption(city_name: str):
    """Get energy consumption data for a city"""
    try:
        data = energy_service.get_energy_consumption(city_name)
        return {
            "success": True,
            "data": data,
            "message": f"Energy consumption data for {city_name} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting energy consumption for {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve energy consumption data")

@router.get("/energy/renewable")
async def get_renewable_energy_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get renewable energy potential and current usage"""
    try:
        data = energy_service.get_renewable_energy_data(lat, lon)
        return {
            "success": True,
            "data": data,
            "message": "Renewable energy data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting renewable energy data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve renewable energy data")

@router.get("/energy/efficiency/{city_name}")
async def get_energy_efficiency_data(city_name: str):
    """Get energy efficiency metrics for a city"""
    try:
        data = energy_service.get_energy_efficiency_data(city_name)
        return {
            "success": True,
            "data": data,
            "message": f"Energy efficiency data for {city_name} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting efficiency data for {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve efficiency data")

@router.get("/energy/smart-grid/{city_name}")
async def get_smart_grid_data(city_name: str):
    """Get smart grid and grid modernization data"""
    try:
        data = energy_service.get_smart_grid_data(city_name)
        return {
            "success": True,
            "data": data,
            "message": f"Smart grid data for {city_name} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting smart grid data for {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve smart grid data")

# Combined Data Endpoints
@router.get("/city-overview/{city_name}")
async def get_city_overview(city_name: str):
    """Get comprehensive city data overview"""
    try:
        # Get coordinates for the city (mock for now)
        city_coords = {
            "San Francisco": {"lat": 37.7749, "lon": -122.4194},
            "Portland": {"lat": 45.5152, "lon": -122.6784},
            "Seattle": {"lat": 47.6062, "lon": -122.3321}
        }
        
        coords = city_coords.get(city_name, {"lat": 37.7749, "lon": -122.4194})
        
        # Fetch all data types
        air_quality = air_quality_service.get_air_quality_by_city(city_name)
        traffic = transportation_service.get_traffic_data(coords["lat"], coords["lon"])
        transit = transportation_service.get_public_transit_data(city_name)
        emissions = transportation_service.get_transportation_emissions(city_name)
        energy_consumption = energy_service.get_energy_consumption(city_name)
        renewable_energy = energy_service.get_renewable_energy_data(coords["lat"], coords["lon"])
        efficiency = energy_service.get_energy_efficiency_data(city_name)
        smart_grid = energy_service.get_smart_grid_data(city_name)
        
        overview = {
            "city": city_name,
            "timestamp": air_quality["timestamp"],
            "location": coords,
            "air_quality": air_quality,
            "transportation": {
                "traffic": traffic,
                "transit": transit,
                "emissions": emissions
            },
            "energy": {
                "consumption": energy_consumption,
                "renewable": renewable_energy,
                "efficiency": efficiency,
                "smart_grid": smart_grid
            },
            "sustainability_score": _calculate_sustainability_score(
                air_quality, traffic, emissions, energy_consumption, renewable_energy
            )
        }
        
        return {
            "success": True,
            "data": overview,
            "message": f"Comprehensive city overview for {city_name} retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error getting city overview for {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve city overview")

@router.get("/data-sources")
async def get_available_data_sources():
    """Get information about available data sources"""
    return {
        "success": True,
        "data": {
            "air_quality": {
                "primary": "OpenWeatherMap API",
                "backup": "AirVisual API",
                "coverage": "Global",
                "update_frequency": "Real-time"
            },
            "transportation": {
                "traffic": "HERE API",
                "transit": "City-specific APIs",
                "bike_share": "City-specific APIs",
                "coverage": "Major cities",
                "update_frequency": "Real-time"
            },
            "energy": {
                "consumption": "EIA API",
                "renewable": "NREL APIs",
                "efficiency": "City utility APIs",
                "coverage": "US cities",
                "update_frequency": "Daily"
            }
        },
        "message": "Data sources information retrieved successfully"
    }

def _calculate_sustainability_score(air_quality: Dict, traffic: Dict, emissions: Dict, 
                                  energy_consumption: Dict, renewable_energy: Dict) -> float:
    """Calculate overall sustainability score"""
    try:
        # Air quality score (0-100)
        aqi = air_quality.get("aqi", 50)
        air_score = max(0, 100 - (aqi - 1) * 25)  # Lower AQI is better
        
        # Transportation score (0-100)
        congestion = traffic.get("congestion_percentage", 30)
        transit_usage = 35  # Mock value
        transport_score = max(0, 100 - congestion + transit_usage * 0.5)
        
        # Energy score (0-100)
        renewable_pct = renewable_energy.get("renewable_percentage", 0.25)
        energy_score = renewable_pct * 100
        
        # Emissions score (0-100)
        emissions_per_capita = emissions.get("per_capita_tonnes", 2.8)
        emissions_score = max(0, 100 - (emissions_per_capita - 1) * 25)
        
        # Weighted average
        sustainability_score = (
            air_score * 0.25 +
            transport_score * 0.30 +
            energy_score * 0.25 +
            emissions_score * 0.20
        )
        
        return round(min(100, max(0, sustainability_score)), 1)
        
    except Exception as e:
        logger.error(f"Error calculating sustainability score: {e}")
        return 75.0  # Default score
