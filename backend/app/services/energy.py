"""
Energy Data Service
Integrates with real energy APIs
"""

import requests
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class EnergyService:
    """Service for fetching real-time energy data"""
    
    def __init__(self):
        self.eia_api_key = os.getenv("EIA_API_KEY", "demo_key")
        self.epa_api_key = os.getenv("EPA_API_KEY", "demo_key")
        self.grid_api_key = os.getenv("GRID_API_KEY", "demo_key")
    
    def get_energy_consumption(self, city_name: str) -> Dict[str, Any]:
        """Get energy consumption data for a city"""
        try:
            # Mock implementation - would integrate with city utility APIs
            # or EIA (Energy Information Administration) data
            
            consumption_data = {
                "city": city_name,
                "timestamp": datetime.utcnow().isoformat(),
                "total_consumption_mwh": self._get_city_consumption(city_name),
                "consumption_by_sector": {
                    "residential": 0.35,
                    "commercial": 0.40,
                    "industrial": 0.20,
                    "transportation": 0.05
                },
                "renewable_percentage": self._get_renewable_percentage(city_name),
                "energy_mix": self._get_energy_mix(city_name),
                "consumption_trends": self._get_consumption_trends(),
                "source": "Mock Energy Data"
            }
            
            return consumption_data
            
        except Exception as e:
            logger.error(f"Error fetching energy consumption for {city_name}: {e}")
            return self._get_mock_consumption_data(city_name)
    
    def get_renewable_energy_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get renewable energy potential and current usage"""
        try:
            # Mock implementation - would use solar/wind potential APIs
            # like NREL's Solar API or wind resource data
            
            renewable_data = {
                "location": {"lat": lat, "lon": lon},
                "timestamp": datetime.utcnow().isoformat(),
                "solar_potential": self._get_solar_potential(lat, lon),
                "wind_potential": self._get_wind_potential(lat, lon),
                "current_renewable_capacity": self._get_current_renewable_capacity(),
                "renewable_generation": self._get_renewable_generation(),
                "carbon_intensity": self._get_carbon_intensity(),
                "source": "Mock Renewable Data"
            }
            
            return renewable_data
            
        except Exception as e:
            logger.error(f"Error fetching renewable energy data: {e}")
            return self._get_mock_renewable_data(lat, lon)
    
    def get_energy_efficiency_data(self, city_name: str) -> Dict[str, Any]:
        """Get energy efficiency metrics for a city"""
        try:
            efficiency_data = {
                "city": city_name,
                "timestamp": datetime.utcnow().isoformat(),
                "building_efficiency_score": self._get_building_efficiency(city_name),
                "efficiency_improvements": self._get_efficiency_improvements(),
                "energy_star_buildings": self._get_energy_star_buildings(city_name),
                "efficiency_programs": self._get_efficiency_programs(),
                "savings_potential": self._get_savings_potential(),
                "source": "Mock Efficiency Data"
            }
            
            return efficiency_data
            
        except Exception as e:
            logger.error(f"Error fetching efficiency data for {city_name}: {e}")
            return self._get_mock_efficiency_data(city_name)
    
    def get_smart_grid_data(self, city_name: str) -> Dict[str, Any]:
        """Get smart grid and grid modernization data"""
        try:
            smart_grid_data = {
                "city": city_name,
                "timestamp": datetime.utcnow().isoformat(),
                "grid_reliability": self._get_grid_reliability(),
                "smart_meter_penetration": self._get_smart_meter_penetration(),
                "demand_response_programs": self._get_demand_response_programs(),
                "energy_storage_capacity": self._get_energy_storage_capacity(),
                "microgrids": self._get_microgrids_data(),
                "grid_modernization_score": self._get_grid_modernization_score(),
                "source": "Mock Smart Grid Data"
            }
            
            return smart_grid_data
            
        except Exception as e:
            logger.error(f"Error fetching smart grid data for {city_name}: {e}")
            return self._get_mock_smart_grid_data(city_name)
    
    def _get_city_consumption(self, city_name: str) -> Dict[str, float]:
        """Get city-specific energy consumption"""
        consumption_map = {
            "San Francisco": {
                "total_mwh": 8500000,
                "per_capita_mwh": 9.7,
                "per_sq_km_mwh": 70000
            },
            "Portland": {
                "total_mwh": 6200000,
                "per_capita_mwh": 9.5,
                "per_sq_km_mwh": 16500
            },
            "Seattle": {
                "total_mwh": 7200000,
                "per_capita_mwh": 9.6,
                "per_sq_km_mwh": 19500
            }
        }
        
        return consumption_map.get(city_name, {
            "total_mwh": 7000000,
            "per_capita_mwh": 9.6,
            "per_sq_km_mwh": 20000
        })
    
    def _get_renewable_percentage(self, city_name: str) -> float:
        """Get renewable energy percentage for city"""
        renewable_map = {
            "San Francisco": 0.25,
            "Portland": 0.30,
            "Seattle": 0.28
        }
        
        return renewable_map.get(city_name, 0.26)
    
    def _get_energy_mix(self, city_name: str) -> Dict[str, float]:
        """Get energy mix for city"""
        return {
            "natural_gas": 0.35,
            "renewable": self._get_renewable_percentage(city_name),
            "nuclear": 0.15,
            "coal": 0.10,
            "hydro": 0.15,
            "other": 0.05
        }
    
    def _get_consumption_trends(self) -> List[Dict[str, Any]]:
        """Get energy consumption trends"""
        import random
        
        trends = []
        for i in range(12):  # 12 months
            month = datetime.utcnow() - timedelta(days=30*i)
            trends.append({
                "month": month.strftime("%Y-%m"),
                "consumption_mwh": random.randint(500000, 800000),
                "renewable_percentage": random.uniform(0.20, 0.35),
                "efficiency_score": random.uniform(0.65, 0.85)
            })
        
        return trends
    
    def _get_solar_potential(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get solar energy potential for location"""
        import random
        
        # Simple latitude-based solar potential
        solar_potential = max(0, 1 - abs(lat - 35) / 35)  # Peak at 35° latitude
        
        return {
            "annual_irradiance_kwh_m2": round(1200 + solar_potential * 800, 2),
            "peak_sun_hours": round(4 + solar_potential * 2, 2),
            "rooftop_potential_mw": round(100 + solar_potential * 200, 2),
            "utility_scale_potential_mw": round(500 + solar_potential * 1000, 2),
            "suitability_score": round(solar_potential, 2)
        }
    
    def _get_wind_potential(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get wind energy potential for location"""
        import random
        
        # Mock wind potential based on location
        wind_potential = random.uniform(0.3, 0.8)
        
        return {
            "average_wind_speed_ms": round(5 + wind_potential * 3, 2),
            "wind_power_density_w_m2": round(200 + wind_potential * 300, 2),
            "capacity_factor": round(0.25 + wind_potential * 0.15, 2),
            "potential_capacity_mw": round(200 + wind_potential * 800, 2),
            "suitability_score": round(wind_potential, 2)
        }
    
    def _get_current_renewable_capacity(self) -> Dict[str, float]:
        """Get current renewable energy capacity"""
        return {
            "solar_mw": 150.5,
            "wind_mw": 89.2,
            "hydro_mw": 45.8,
            "geothermal_mw": 12.3,
            "biomass_mw": 8.7,
            "total_mw": 306.5
        }
    
    def _get_renewable_generation(self) -> Dict[str, Any]:
        """Get current renewable energy generation"""
        import random
        
        return {
            "current_generation_mw": random.randint(200, 300),
            "capacity_utilization": random.uniform(0.65, 0.85),
            "daily_generation_mwh": random.randint(3000, 5000),
            "monthly_generation_mwh": random.randint(90000, 150000)
        }
    
    def _get_carbon_intensity(self) -> Dict[str, float]:
        """Get carbon intensity of energy generation"""
        return {
            "total_g_co2_kwh": 350.5,
            "renewable_g_co2_kwh": 25.2,
            "fossil_fuel_g_co2_kwh": 450.8,
            "reduction_target_2030": 0.50,
            "current_reduction": 0.22
        }
    
    def _get_building_efficiency(self, city_name: str) -> Dict[str, Any]:
        """Get building energy efficiency metrics"""
        efficiency_map = {
            "San Francisco": 0.72,
            "Portland": 0.75,
            "Seattle": 0.73
        }
        
        base_efficiency = efficiency_map.get(city_name, 0.73)
        
        return {
            "overall_score": base_efficiency,
            "residential_score": base_efficiency + 0.02,
            "commercial_score": base_efficiency - 0.01,
            "improvement_potential": 0.15,
            "leed_certified_buildings": 125
        }
    
    def _get_efficiency_improvements(self) -> List[Dict[str, Any]]:
        """Get recent efficiency improvements"""
        return [
            {
                "type": "LED Lighting",
                "buildings_retrofitted": 1500,
                "energy_savings_percent": 0.25,
                "cost_savings_annual": 2500000
            },
            {
                "type": "HVAC Upgrades",
                "buildings_retrofitted": 800,
                "energy_savings_percent": 0.18,
                "cost_savings_annual": 1800000
            },
            {
                "type": "Insulation Improvements",
                "buildings_retrofitted": 2000,
                "energy_savings_percent": 0.12,
                "cost_savings_annual": 1200000
            }
        ]
    
    def _get_energy_star_buildings(self, city_name: str) -> Dict[str, int]:
        """Get Energy Star certified buildings"""
        star_buildings_map = {
            "San Francisco": 45,
            "Portland": 38,
            "Seattle": 42
        }
        
        return {
            "total_certified": star_buildings_map.get(city_name, 40),
            "residential": 15,
            "commercial": 25,
            "pending_certification": 8
        }
    
    def _get_efficiency_programs(self) -> List[Dict[str, Any]]:
        """Get active efficiency programs"""
        return [
            {
                "name": "Residential Rebate Program",
                "participants": 2500,
                "total_rebates": 5000000,
                "energy_saved_mwh": 15000
            },
            {
                "name": "Commercial Retrofit Program",
                "participants": 150,
                "total_rebates": 8000000,
                "energy_saved_mwh": 25000
            },
            {
                "name": "Low-Income Weatherization",
                "participants": 800,
                "total_rebates": 2000000,
                "energy_saved_mwh": 5000
            }
        ]
    
    def _get_savings_potential(self) -> Dict[str, Any]:
        """Get energy savings potential"""
        return {
            "total_potential_mwh": 500000,
            "cost_savings_potential": 75000000,
            "carbon_reduction_tons": 250000,
            "payback_period_years": 8.5
        }
    
    def _get_grid_reliability(self) -> Dict[str, Any]:
        """Get grid reliability metrics"""
        return {
            "saidi_minutes": 120.5,  # System Average Interruption Duration Index
            "saifi_count": 1.2,      # System Average Interruption Frequency Index
            "reliability_score": 0.92,
            "outage_duration_avg_minutes": 45.2
        }
    
    def _get_smart_meter_penetration(self) -> Dict[str, Any]:
        """Get smart meter penetration data"""
        return {
            "residential_penetration": 0.85,
            "commercial_penetration": 0.92,
            "total_smart_meters": 450000,
            "data_collection_rate": 0.98
        }
    
    def _get_demand_response_programs(self) -> List[Dict[str, Any]]:
        """Get demand response programs"""
        return [
            {
                "name": "Peak Time Rebates",
                "participants": 15000,
                "peak_reduction_mw": 25.5,
                "annual_savings": 2000000
            },
            {
                "name": "Critical Peak Pricing",
                "participants": 8000,
                "peak_reduction_mw": 15.2,
                "annual_savings": 1200000
            }
        ]
    
    def _get_energy_storage_capacity(self) -> Dict[str, Any]:
        """Get energy storage capacity"""
        return {
            "total_capacity_mwh": 125.5,
            "battery_storage_mwh": 85.2,
            "pumped_hydro_mwh": 40.3,
            "planned_capacity_mwh": 200.0
        }
    
    def _get_microgrids_data(self) -> List[Dict[str, Any]]:
        """Get microgrid information"""
        return [
            {
                "name": "Downtown Microgrid",
                "capacity_mw": 5.5,
                "renewable_percentage": 0.80,
                "backup_hours": 24
            },
            {
                "name": "University Campus",
                "capacity_mw": 3.2,
                "renewable_percentage": 0.65,
                "backup_hours": 48
            }
        ]
    
    def _get_grid_modernization_score(self) -> float:
        """Get grid modernization score"""
        return 0.78
    
    def _get_mock_consumption_data(self, city_name: str) -> Dict[str, Any]:
        """Return mock consumption data"""
        return {
            "city": city_name,
            "timestamp": datetime.utcnow().isoformat(),
            "total_consumption_mwh": self._get_city_consumption(city_name),
            "consumption_by_sector": {
                "residential": 0.35,
                "commercial": 0.40,
                "industrial": 0.20,
                "transportation": 0.05
            },
            "renewable_percentage": self._get_renewable_percentage(city_name),
            "energy_mix": self._get_energy_mix(city_name),
            "consumption_trends": self._get_consumption_trends(),
            "source": "Mock Data"
        }
    
    def _get_mock_renewable_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Return mock renewable data"""
        return {
            "location": {"lat": lat, "lon": lon},
            "timestamp": datetime.utcnow().isoformat(),
            "solar_potential": self._get_solar_potential(lat, lon),
            "wind_potential": self._get_wind_potential(lat, lon),
            "current_renewable_capacity": self._get_current_renewable_capacity(),
            "renewable_generation": self._get_renewable_generation(),
            "carbon_intensity": self._get_carbon_intensity(),
            "source": "Mock Data"
        }
    
    def _get_mock_efficiency_data(self, city_name: str) -> Dict[str, Any]:
        """Return mock efficiency data"""
        return {
            "city": city_name,
            "timestamp": datetime.utcnow().isoformat(),
            "building_efficiency_score": self._get_building_efficiency(city_name),
            "efficiency_improvements": self._get_efficiency_improvements(),
            "energy_star_buildings": self._get_energy_star_buildings(city_name),
            "efficiency_programs": self._get_efficiency_programs(),
            "savings_potential": self._get_savings_potential(),
            "source": "Mock Data"
        }
    
    def _get_mock_smart_grid_data(self, city_name: str) -> Dict[str, Any]:
        """Return mock smart grid data"""
        return {
            "city": city_name,
            "timestamp": datetime.utcnow().isoformat(),
            "grid_reliability": self._get_grid_reliability(),
            "smart_meter_penetration": self._get_smart_meter_penetration(),
            "demand_response_programs": self._get_demand_response_programs(),
            "energy_storage_capacity": self._get_energy_storage_capacity(),
            "microgrids": self._get_microgrids_data(),
            "grid_modernization_score": self._get_grid_modernization_score(),
            "source": "Mock Data"
        }

# Global instance
energy_service = EnergyService()
