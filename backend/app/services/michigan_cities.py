"""
Michigan Cities Data Service
Comprehensive data for all major Michigan cities
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MichiganCitiesService:
    """Service for Michigan cities data and analysis"""
    
    def __init__(self):
        self.michigan_cities = self._initialize_michigan_cities()
    
    def _initialize_michigan_cities(self) -> List[Dict[str, Any]]:
        """Initialize comprehensive Michigan cities data"""
        return [
            {
                "id": 1,
                "name": "Detroit",
                "state": "MI",
                "population": 639111,
                "area_km2": 370.0,
                "coordinates": {"lat": 42.3314, "lon": -83.0458},
                "emissions_tonnes_co2": 8200000,
                "air_quality_index": 55,
                "sustainability_score": 65,
                "public_transit_usage": 12,
                "car_ownership_rate": 0.85,
                "bike_lane_km": 45,
                "green_space_percent": 8,
                "energy_renewable_percent": 15,
                "building_efficiency": 0.55,
                "median_income": 32000,
                "unemployment_rate": 8.5,
                "key_industries": ["Automotive", "Manufacturing", "Healthcare"],
                "challenges": ["Urban decay", "High unemployment", "Air quality"],
                "opportunities": ["Waterfront development", "Tech sector growth", "Green infrastructure"]
            },
            {
                "id": 2,
                "name": "Grand Rapids",
                "state": "MI",
                "population": 198917,
                "area_km2": 117.4,
                "coordinates": {"lat": 42.9634, "lon": -85.6681},
                "emissions_tonnes_co2": 2100000,
                "air_quality_index": 42,
                "sustainability_score": 78,
                "public_transit_usage": 8,
                "car_ownership_rate": 0.78,
                "bike_lane_km": 85,
                "green_space_percent": 15,
                "energy_renewable_percent": 22,
                "building_efficiency": 0.68,
                "median_income": 45000,
                "unemployment_rate": 4.2,
                "key_industries": ["Manufacturing", "Healthcare", "Technology"],
                "challenges": ["Sprawl", "Transportation", "Affordable housing"],
                "opportunities": ["Downtown revitalization", "Tech hub", "Green energy"]
            },
            {
                "id": 3,
                "name": "Warren",
                "state": "MI",
                "population": 139387,
                "area_km2": 89.2,
                "coordinates": {"lat": 42.5145, "lon": -83.0147},
                "emissions_tonnes_co2": 1800000,
                "air_quality_index": 48,
                "sustainability_score": 72,
                "public_transit_usage": 5,
                "car_ownership_rate": 0.88,
                "bike_lane_km": 25,
                "green_space_percent": 12,
                "energy_renewable_percent": 18,
                "building_efficiency": 0.62,
                "median_income": 52000,
                "unemployment_rate": 5.8,
                "key_industries": ["Automotive", "Defense", "Manufacturing"],
                "challenges": ["Industrial pollution", "Traffic congestion", "Aging infrastructure"],
                "opportunities": ["Green manufacturing", "Transit-oriented development", "Clean energy"]
            },
            {
                "id": 4,
                "name": "Sterling Heights",
                "state": "MI",
                "population": 134346,
                "area_km2": 95.3,
                "coordinates": {"lat": 42.5803, "lon": -83.0302},
                "emissions_tonnes_co2": 1600000,
                "air_quality_index": 45,
                "sustainability_score": 75,
                "public_transit_usage": 6,
                "car_ownership_rate": 0.82,
                "bike_lane_km": 35,
                "green_space_percent": 14,
                "energy_renewable_percent": 20,
                "building_efficiency": 0.65,
                "median_income": 58000,
                "unemployment_rate": 4.5,
                "key_industries": ["Automotive", "Technology", "Healthcare"],
                "challenges": ["Suburban sprawl", "Transportation", "Water management"],
                "opportunities": ["Smart city initiatives", "Green building", "Community connectivity"]
            },
            {
                "id": 5,
                "name": "Lansing",
                "state": "MI",
                "population": 118210,
                "area_km2": 102.4,
                "coordinates": {"lat": 42.7325, "lon": -84.5555},
                "emissions_tonnes_co2": 1400000,
                "air_quality_index": 38,
                "sustainability_score": 80,
                "public_transit_usage": 15,
                "car_ownership_rate": 0.75,
                "bike_lane_km": 65,
                "green_space_percent": 18,
                "energy_renewable_percent": 25,
                "building_efficiency": 0.70,
                "median_income": 42000,
                "unemployment_rate": 4.8,
                "key_industries": ["Government", "Education", "Healthcare"],
                "challenges": ["Economic diversification", "Infrastructure", "Housing affordability"],
                "opportunities": ["State capital development", "University partnerships", "Green infrastructure"]
            },
            {
                "id": 6,
                "name": "Ann Arbor",
                "state": "MI",
                "population": 123851,
                "area_km2": 74.3,
                "coordinates": {"lat": 42.2808, "lon": -83.7430},
                "emissions_tonnes_co2": 1200000,
                "air_quality_index": 35,
                "sustainability_score": 88,
                "public_transit_usage": 25,
                "car_ownership_rate": 0.65,
                "bike_lane_km": 120,
                "green_space_percent": 22,
                "energy_renewable_percent": 35,
                "building_efficiency": 0.78,
                "median_income": 65000,
                "unemployment_rate": 3.2,
                "key_industries": ["Education", "Technology", "Healthcare"],
                "challenges": ["Housing costs", "Traffic congestion", "Gentrification"],
                "opportunities": ["Innovation hub", "Sustainable transportation", "Green building"]
            },
            {
                "id": 7,
                "name": "Flint",
                "state": "MI",
                "population": 95138,
                "area_km2": 88.2,
                "coordinates": {"lat": 43.0125, "lon": -83.6875},
                "emissions_tonnes_co2": 1800000,
                "air_quality_index": 65,
                "sustainability_score": 58,
                "public_transit_usage": 8,
                "car_ownership_rate": 0.82,
                "bike_lane_km": 20,
                "green_space_percent": 10,
                "energy_renewable_percent": 12,
                "building_efficiency": 0.50,
                "median_income": 28000,
                "unemployment_rate": 12.5,
                "key_industries": ["Manufacturing", "Healthcare", "Education"],
                "challenges": ["Water crisis", "Economic decline", "Environmental justice"],
                "opportunities": ["Water infrastructure", "Economic revitalization", "Community resilience"]
            },
            {
                "id": 8,
                "name": "Dearborn",
                "state": "MI",
                "population": 109976,
                "area_km2": 63.4,
                "coordinates": {"lat": 42.3223, "lon": -83.1763},
                "emissions_tonnes_co2": 1900000,
                "air_quality_index": 52,
                "sustainability_score": 70,
                "public_transit_usage": 10,
                "car_ownership_rate": 0.80,
                "bike_lane_km": 30,
                "green_space_percent": 12,
                "energy_renewable_percent": 16,
                "building_efficiency": 0.60,
                "median_income": 48000,
                "unemployment_rate": 6.2,
                "key_industries": ["Automotive", "Manufacturing", "Healthcare"],
                "challenges": ["Industrial pollution", "Traffic", "Housing diversity"],
                "opportunities": ["Green manufacturing", "Cultural diversity", "Transit development"]
            },
            {
                "id": 9,
                "name": "Livonia",
                "state": "MI",
                "population": 95068,
                "area_km2": 92.9,
                "coordinates": {"lat": 42.3684, "lon": -83.3527},
                "emissions_tonnes_co2": 1300000,
                "air_quality_index": 44,
                "sustainability_score": 73,
                "public_transit_usage": 7,
                "car_ownership_rate": 0.85,
                "bike_lane_km": 40,
                "green_space_percent": 16,
                "energy_renewable_percent": 19,
                "building_efficiency": 0.67,
                "median_income": 55000,
                "unemployment_rate": 4.8,
                "key_industries": ["Healthcare", "Manufacturing", "Technology"],
                "challenges": ["Suburban sprawl", "Transportation", "Aging population"],
                "opportunities": ["Healthcare hub", "Green infrastructure", "Community services"]
            },
            {
                "id": 10,
                "name": "Westland",
                "state": "MI",
                "population": 85000,
                "area_km2": 52.8,
                "coordinates": {"lat": 42.3242, "lon": -83.4002},
                "emissions_tonnes_co2": 1100000,
                "air_quality_index": 46,
                "sustainability_score": 68,
                "public_transit_usage": 6,
                "car_ownership_rate": 0.83,
                "bike_lane_km": 25,
                "green_space_percent": 13,
                "energy_renewable_percent": 17,
                "building_efficiency": 0.63,
                "median_income": 45000,
                "unemployment_rate": 5.5,
                "key_industries": ["Manufacturing", "Retail", "Healthcare"],
                "challenges": ["Economic development", "Infrastructure", "Community engagement"],
                "opportunities": ["Downtown revitalization", "Green building", "Transit connectivity"]
            }
            # Additional cities would continue here...
        ]
    
    def get_all_cities(self) -> List[Dict[str, Any]]:
        """Get all Michigan cities"""
        return self.michigan_cities
    
    def get_city_by_name(self, city_name: str) -> Optional[Dict[str, Any]]:
        """Get specific city by name"""
        for city in self.michigan_cities:
            if city["name"].lower() == city_name.lower():
                return city
        return None
    
    def get_cities_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Get cities by region (Southeast, West, Central, etc.)"""
        region_mapping = {
            "southeast": ["Detroit", "Warren", "Sterling Heights", "Dearborn", "Livonia", "Westland", "Taylor", "Pontiac", "St. Clair Shores", "Royal Oak", "Novi", "Dearborn Heights", "Roseville", "Lincoln Park"],
            "west": ["Grand Rapids", "Kalamazoo", "Wyoming", "Kentwood", "Portage", "Battle Creek"],
            "central": ["Lansing", "East Lansing", "Flint", "Saginaw", "Midland"],
            "north": ["Traverse City", "Marquette", "Sault Ste. Marie"]
        }
        
        region_cities = region_mapping.get(region.lower(), [])
        return [city for city in self.michigan_cities if city["name"] in region_cities]
    
    def get_sustainability_ranking(self) -> List[Dict[str, Any]]:
        """Get cities ranked by sustainability score"""
        return sorted(self.michigan_cities, key=lambda x: x["sustainability_score"], reverse=True)
    
    def get_emissions_ranking(self) -> List[Dict[str, Any]]:
        """Get cities ranked by emissions (lowest first)"""
        return sorted(self.michigan_cities, key=lambda x: x["emissions_tonnes_co2"])
    
    def get_cities_by_population_range(self, min_pop: int, max_pop: int) -> List[Dict[str, Any]]:
        """Get cities within population range"""
        return [city for city in self.michigan_cities if min_pop <= city["population"] <= max_pop]
    
    def get_michigan_statistics(self) -> Dict[str, Any]:
        """Get overall Michigan statistics"""
        total_population = sum(city["population"] for city in self.michigan_cities)
        total_emissions = sum(city["emissions_tonnes_co2"] for city in self.michigan_cities)
        avg_sustainability = sum(city["sustainability_score"] for city in self.michigan_cities) / len(self.michigan_cities)
        avg_air_quality = sum(city["air_quality_index"] for city in self.michigan_cities) / len(self.michigan_cities)
        
        return {
            "total_cities": len(self.michigan_cities),
            "total_population": total_population,
            "total_emissions_tonnes_co2": total_emissions,
            "average_sustainability_score": round(avg_sustainability, 1),
            "average_air_quality_index": round(avg_air_quality, 1),
            "emissions_per_capita": round(total_emissions / total_population, 2),
            "most_sustainable_city": max(self.michigan_cities, key=lambda x: x["sustainability_score"])["name"],
            "least_sustainable_city": min(self.michigan_cities, key=lambda x: x["sustainability_score"])["name"],
            "largest_city": max(self.michigan_cities, key=lambda x: x["population"])["name"],
            "smallest_city": min(self.michigan_cities, key=lambda x: x["population"])["name"]
        }
    
    def get_policy_recommendations_for_city(self, city_name: str) -> List[Dict[str, Any]]:
        """Get specific policy recommendations for a Michigan city"""
        city = self.get_city_by_name(city_name)
        if not city:
            return []
        
        recommendations = []
        
        # Air quality recommendations
        if city["air_quality_index"] > 50:
            recommendations.append({
                "type": "environmental",
                "priority": "high",
                "title": "Improve Air Quality",
                "description": f"Current AQI is {city['air_quality_index']}. Implement green infrastructure and reduce industrial emissions.",
                "estimated_impact": "15-25% AQI improvement",
                "cost_range": "$5M - $15M"
            })
        
        # Transportation recommendations
        if city["public_transit_usage"] < 15:
            recommendations.append({
                "type": "transportation",
                "priority": "medium",
                "title": "Expand Public Transit",
                "description": f"Current transit usage is {city['public_transit_usage']}%. Expand bus routes and improve frequency.",
                "estimated_impact": "10-20% increase in ridership",
                "cost_range": "$10M - $30M"
            })
        
        # Green space recommendations
        if city["green_space_percent"] < 15:
            recommendations.append({
                "type": "environmental",
                "priority": "medium",
                "title": "Increase Green Space",
                "description": f"Current green space is {city['green_space_percent']}%. Create parks and green corridors.",
                "estimated_impact": "5-10% improvement in air quality",
                "cost_range": "$3M - $10M"
            })
        
        # Energy efficiency recommendations
        if city["energy_renewable_percent"] < 20:
            recommendations.append({
                "type": "energy",
                "priority": "high",
                "title": "Increase Renewable Energy",
                "description": f"Current renewable energy is {city['energy_renewable_percent']}%. Install solar and wind projects.",
                "estimated_impact": "20-30% emissions reduction",
                "cost_range": "$15M - $50M"
            })
        
        return recommendations

# Global instance
michigan_cities_service = MichiganCitiesService()
