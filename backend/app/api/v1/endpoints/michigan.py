"""
Michigan Cities API Endpoints
Specialized endpoints for Michigan cities analysis
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any, Optional
import logging
from ...services.michigan_cities import michigan_cities_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/cities")
async def get_all_michigan_cities():
    """Get all Michigan cities with comprehensive data"""
    try:
        cities = michigan_cities_service.get_all_cities()
        return {
            "success": True,
            "data": cities,
            "count": len(cities),
            "message": f"Retrieved {len(cities)} Michigan cities"
        }
    except Exception as e:
        logger.error(f"Error getting Michigan cities: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Michigan cities")

@router.get("/cities/{city_name}")
async def get_michigan_city(city_name: str):
    """Get specific Michigan city data"""
    try:
        city = michigan_cities_service.get_city_by_name(city_name)
        if not city:
            raise HTTPException(status_code=404, detail=f"City '{city_name}' not found in Michigan")
        
        return {
            "success": True,
            "data": city,
            "message": f"Retrieved data for {city_name}, Michigan"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting city {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve city data")

@router.get("/cities/region/{region}")
async def get_cities_by_region(region: str):
    """Get Michigan cities by region"""
    try:
        cities = michigan_cities_service.get_cities_by_region(region)
        return {
            "success": True,
            "data": cities,
            "count": len(cities),
            "region": region,
            "message": f"Retrieved {len(cities)} cities from {region} Michigan"
        }
    except Exception as e:
        logger.error(f"Error getting cities by region {region}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve cities by region")

@router.get("/rankings/sustainability")
async def get_sustainability_ranking():
    """Get Michigan cities ranked by sustainability score"""
    try:
        ranking = michigan_cities_service.get_sustainability_ranking()
        return {
            "success": True,
            "data": ranking,
            "message": "Michigan cities ranked by sustainability score"
        }
    except Exception as e:
        logger.error(f"Error getting sustainability ranking: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sustainability ranking")

@router.get("/rankings/emissions")
async def get_emissions_ranking():
    """Get Michigan cities ranked by emissions (lowest first)"""
    try:
        ranking = michigan_cities_service.get_emissions_ranking()
        return {
            "success": True,
            "data": ranking,
            "message": "Michigan cities ranked by emissions (lowest first)"
        }
    except Exception as e:
        logger.error(f"Error getting emissions ranking: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve emissions ranking")

@router.get("/statistics")
async def get_michigan_statistics():
    """Get overall Michigan statistics"""
    try:
        stats = michigan_cities_service.get_michigan_statistics()
        return {
            "success": True,
            "data": stats,
            "message": "Michigan cities overall statistics"
        }
    except Exception as e:
        logger.error(f"Error getting Michigan statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Michigan statistics")

@router.get("/cities/{city_name}/recommendations")
async def get_city_recommendations(city_name: str):
    """Get policy recommendations for a specific Michigan city"""
    try:
        recommendations = michigan_cities_service.get_policy_recommendations_for_city(city_name)
        if not recommendations:
            raise HTTPException(status_code=404, detail=f"No recommendations found for {city_name}")
        
        return {
            "success": True,
            "data": {
                "city": city_name,
                "recommendations": recommendations,
                "count": len(recommendations)
            },
            "message": f"Policy recommendations for {city_name}, Michigan"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recommendations for {city_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve city recommendations")

@router.get("/cities/population-range")
async def get_cities_by_population(
    min_population: int = Query(..., description="Minimum population"),
    max_population: int = Query(..., description="Maximum population")
):
    """Get Michigan cities within population range"""
    try:
        cities = michigan_cities_service.get_cities_by_population_range(min_population, max_population)
        return {
            "success": True,
            "data": cities,
            "count": len(cities),
            "population_range": f"{min_population:,} - {max_population:,}",
            "message": f"Found {len(cities)} Michigan cities in population range"
        }
    except Exception as e:
        logger.error(f"Error getting cities by population range: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve cities by population range")

@router.get("/comparison")
async def compare_michigan_cities(
    cities: str = Query(..., description="Comma-separated list of city names")
):
    """Compare multiple Michigan cities"""
    try:
        city_names = [name.strip() for name in cities.split(",")]
        city_data = []
        
        for city_name in city_names:
            city = michigan_cities_service.get_city_by_name(city_name)
            if city:
                city_data.append(city)
            else:
                logger.warning(f"City {city_name} not found")
        
        if not city_data:
            raise HTTPException(status_code=404, detail="No valid cities found for comparison")
        
        # Create comparison summary
        comparison = {
            "cities": city_data,
            "summary": {
                "most_sustainable": max(city_data, key=lambda x: x["sustainability_score"])["name"],
                "least_sustainable": min(city_data, key=lambda x: x["sustainability_score"])["name"],
                "highest_emissions": max(city_data, key=lambda x: x["emissions_tonnes_co2"])["name"],
                "lowest_emissions": min(city_data, key=lambda x: x["emissions_tonnes_co2"])["name"],
                "best_air_quality": min(city_data, key=lambda x: x["air_quality_index"])["name"],
                "worst_air_quality": max(city_data, key=lambda x: x["air_quality_index"])["name"]
            }
        }
        
        return {
            "success": True,
            "data": comparison,
            "message": f"Comparison of {len(city_data)} Michigan cities"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing cities: {e}")
        raise HTTPException(status_code=500, detail="Failed to compare cities")

@router.get("/insights")
async def get_michigan_insights():
    """Get key insights about Michigan cities sustainability"""
    try:
        stats = michigan_cities_service.get_michigan_statistics()
        sustainability_ranking = michigan_cities_service.get_sustainability_ranking()
        
        insights = {
            "overview": stats,
            "top_performers": sustainability_ranking[:5],
            "bottom_performers": sustainability_ranking[-5:],
            "key_insights": [
                f"Michigan's most sustainable city is {stats['most_sustainable_city']} with a score of {max(sustainability_ranking, key=lambda x: x['sustainability_score'])['sustainability_score']}/100",
                f"Average sustainability score across Michigan cities is {stats['average_sustainability_score']}/100",
                f"Total population across {stats['total_cities']} cities is {stats['total_population']:,} people",
                f"Combined annual emissions are {stats['total_emissions_tonnes_co2']:,} tons CO₂",
                f"Average air quality index is {stats['average_air_quality_index']} (lower is better)"
            ],
            "recommendations": [
                "Focus on improving public transit in larger cities like Detroit and Grand Rapids",
                "Increase renewable energy adoption across all cities",
                "Expand green infrastructure in urban areas",
                "Address air quality issues in industrial cities",
                "Promote sustainable transportation options"
            ]
        }
        
        return {
            "success": True,
            "data": insights,
            "message": "Michigan cities sustainability insights"
        }
    except Exception as e:
        logger.error(f"Error getting Michigan insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Michigan insights")
