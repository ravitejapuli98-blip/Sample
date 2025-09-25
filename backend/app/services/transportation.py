"""
Transportation Data Service
Integrates with real transportation APIs
"""

import requests
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class TransportationService:
    """Service for fetching real-time transportation data"""
    
    def __init__(self):
        self.google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY", "demo_key")
        self.here_api_key = os.getenv("HERE_API_KEY", "demo_key")
        self.transit_api_key = os.getenv("TRANSIT_API_KEY", "demo_key")
    
    def get_traffic_data(self, lat: float, lon: float, radius: int = 5000) -> Dict[str, Any]:
        """Get real-time traffic data for a location"""
        try:
            # Using HERE API for traffic data
            url = "https://traffic.ls.hereapi.com/traffic/6.3/flow.json"
            params = {
                "apiKey": self.here_api_key,
                "bbox": f"{lat-0.05},{lon-0.05},{lat+0.05},{lon+0.05}",
                "responseattributes": "sh,fc"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process traffic flow data
            traffic_flows = data.get("RWS", [{}])[0].get("RW", [])
            total_flows = len(traffic_flows)
            
            # Calculate average speed and congestion
            speeds = []
            congestion_levels = []
            
            for flow in traffic_flows:
                for f in flow.get("FIS", [{}])[0].get("FI", []):
                    speed = f.get("CF", [{}])[0].get("FF", 0)  # Free flow speed
                    current_speed = f.get("CF", [{}])[0].get("JF", 0)  # Current speed
                    
                    if speed > 0 and current_speed > 0:
                        speeds.append(current_speed)
                        congestion = max(0, (speed - current_speed) / speed * 100)
                        congestion_levels.append(congestion)
            
            avg_speed = sum(speeds) / len(speeds) if speeds else 0
            avg_congestion = sum(congestion_levels) / len(congestion_levels) if congestion_levels else 0
            
            return {
                "location": {"lat": lat, "lon": lon},
                "timestamp": datetime.utcnow().isoformat(),
                "traffic_flows": total_flows,
                "average_speed_kmh": round(avg_speed, 2),
                "congestion_percentage": round(avg_congestion, 2),
                "congestion_level": self._get_congestion_level(avg_congestion),
                "source": "HERE API"
            }
            
        except requests.RequestException as e:
            logger.error(f"Error fetching traffic data: {e}")
            return self._get_mock_traffic_data(lat, lon)
        except Exception as e:
            logger.error(f"Unexpected error in transportation service: {e}")
            return self._get_mock_traffic_data(lat, lon)
    
    def get_public_transit_data(self, city_name: str) -> Dict[str, Any]:
        """Get public transit information for a city"""
        try:
            # Mock implementation - in real scenario, would use city-specific transit APIs
            # like BART API for San Francisco, MTA API for NYC, etc.
            
            transit_data = {
                "city": city_name,
                "timestamp": datetime.utcnow().isoformat(),
                "systems": self._get_city_transit_systems(city_name),
                "ridership": self._get_mock_ridership_data(city_name),
                "delays": self._get_mock_delay_data(),
                "source": "Mock Transit Data"
            }
            
            return transit_data
            
        except Exception as e:
            logger.error(f"Error fetching transit data for {city_name}: {e}")
            return self._get_mock_transit_data(city_name)
    
    def get_bike_share_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get bike share station data"""
        try:
            # Mock implementation - would integrate with city bike share APIs
            # like Citi Bike API for NYC, Bay Wheels for SF, etc.
            
            bike_data = {
                "location": {"lat": lat, "lon": lon},
                "timestamp": datetime.utcnow().isoformat(),
                "stations": self._get_mock_bike_stations(lat, lon),
                "total_bikes": 150,
                "total_docks": 200,
                "utilization_rate": 0.75,
                "source": "Mock Bike Share Data"
            }
            
            return bike_data
            
        except Exception as e:
            logger.error(f"Error fetching bike share data: {e}")
            return self._get_mock_bike_data(lat, lon)
    
    def get_transportation_emissions(self, city_name: str) -> Dict[str, Any]:
        """Get transportation-related emissions data"""
        try:
            # Mock implementation - would use EPA or city-specific emissions data
            
            emissions_data = {
                "city": city_name,
                "timestamp": datetime.utcnow().isoformat(),
                "total_transportation_emissions": self._get_city_emissions(city_name),
                "emissions_by_mode": {
                    "private_vehicles": 0.65,
                    "public_transit": 0.15,
                    "commercial_vehicles": 0.15,
                    "aviation": 0.05
                },
                "emissions_trends": self._get_emissions_trends(),
                "source": "Mock Emissions Data"
            }
            
            return emissions_data
            
        except Exception as e:
            logger.error(f"Error fetching emissions data for {city_name}: {e}")
            return self._get_mock_emissions_data(city_name)
    
    def _get_congestion_level(self, congestion_percentage: float) -> str:
        """Convert congestion percentage to level description"""
        if congestion_percentage < 20:
            return "Light"
        elif congestion_percentage < 40:
            return "Moderate"
        elif congestion_percentage < 60:
            return "Heavy"
        else:
            return "Severe"
    
    def _get_city_transit_systems(self, city_name: str) -> List[Dict[str, Any]]:
        """Get transit systems for a city"""
        systems_map = {
            "San Francisco": [
                {"name": "BART", "type": "Rail", "lines": 5, "stations": 50},
                {"name": "Muni", "type": "Bus/Light Rail", "lines": 20, "stations": 200},
                {"name": "Cable Car", "type": "Historic", "lines": 3, "stations": 8}
            ],
            "Portland": [
                {"name": "MAX", "type": "Light Rail", "lines": 5, "stations": 97},
                {"name": "TriMet Bus", "type": "Bus", "lines": 80, "stations": 5000},
                {"name": "Streetcar", "type": "Streetcar", "lines": 2, "stations": 30}
            ],
            "Seattle": [
                {"name": "Link Light Rail", "type": "Light Rail", "lines": 1, "stations": 19},
                {"name": "Sound Transit", "type": "Commuter Rail", "lines": 2, "stations": 12},
                {"name": "King County Metro", "type": "Bus", "lines": 200, "stations": 8000}
            ]
        }
        
        return systems_map.get(city_name, [
            {"name": "Local Transit", "type": "Bus", "lines": 10, "stations": 100}
        ])
    
    def _get_mock_ridership_data(self, city_name: str) -> Dict[str, Any]:
        """Get mock ridership data"""
        import random
        
        return {
            "daily_riders": random.randint(500000, 2000000),
            "monthly_riders": random.randint(15000000, 60000000),
            "ridership_change_yoy": random.uniform(-0.05, 0.15),
            "peak_hours": {
                "morning": "7:00-9:00 AM",
                "evening": "5:00-7:00 PM"
            },
            "most_popular_routes": [
                {"route": "Downtown Express", "riders": random.randint(50000, 100000)},
                {"route": "Airport Shuttle", "riders": random.randint(30000, 80000)},
                {"route": "University Line", "riders": random.randint(40000, 90000)}
            ]
        }
    
    def _get_mock_delay_data(self) -> List[Dict[str, Any]]:
        """Get mock delay information"""
        import random
        
        delays = []
        for i in range(random.randint(0, 5)):
            delays.append({
                "line": f"Line {chr(65 + i)}",
                "delay_minutes": random.randint(5, 30),
                "reason": random.choice([
                    "Signal problem",
                    "Mechanical issue",
                    "Weather conditions",
                    "Police activity"
                ]),
                "affected_stations": random.randint(2, 8)
            })
        
        return delays
    
    def _get_mock_bike_stations(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Get mock bike share stations"""
        import random
        
        stations = []
        for i in range(random.randint(5, 15)):
            stations.append({
                "id": f"station_{i}",
                "name": f"Station {i+1}",
                "location": {
                    "lat": lat + random.uniform(-0.01, 0.01),
                    "lon": lon + random.uniform(-0.01, 0.01)
                },
                "bikes_available": random.randint(0, 20),
                "docks_available": random.randint(0, 25),
                "status": random.choice(["Active", "Active", "Active", "Maintenance"])
            })
        
        return stations
    
    def _get_city_emissions(self, city_name: str) -> Dict[str, float]:
        """Get city-specific transportation emissions"""
        emissions_map = {
            "San Francisco": {
                "total_co2_tonnes": 2500000,
                "per_capita_tonnes": 2.86,
                "transportation_percent": 0.45
            },
            "Portland": {
                "total_co2_tonnes": 1800000,
                "per_capita_tonnes": 2.76,
                "transportation_percent": 0.40
            },
            "Seattle": {
                "total_co2_tonnes": 2200000,
                "per_capita_tonnes": 2.94,
                "transportation_percent": 0.42
            }
        }
        
        return emissions_map.get(city_name, {
            "total_co2_tonnes": 2000000,
            "per_capita_tonnes": 2.80,
            "transportation_percent": 0.43
        })
    
    def _get_emissions_trends(self) -> List[Dict[str, Any]]:
        """Get emissions trends over time"""
        import random
        
        trends = []
        for i in range(12):  # 12 months
            month = datetime.utcnow() - timedelta(days=30*i)
            trends.append({
                "month": month.strftime("%Y-%m"),
                "emissions_tonnes": random.randint(180000, 220000),
                "change_from_previous": random.uniform(-0.05, 0.05)
            })
        
        return trends
    
    def _get_mock_traffic_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Return mock traffic data"""
        import random
        
        return {
            "location": {"lat": lat, "lon": lon},
            "timestamp": datetime.utcnow().isoformat(),
            "traffic_flows": random.randint(50, 200),
            "average_speed_kmh": round(random.uniform(25, 65), 2),
            "congestion_percentage": round(random.uniform(10, 60), 2),
            "congestion_level": random.choice(["Light", "Moderate", "Heavy"]),
            "source": "Mock Data"
        }
    
    def _get_mock_transit_data(self, city_name: str) -> Dict[str, Any]:
        """Return mock transit data"""
        return {
            "city": city_name,
            "timestamp": datetime.utcnow().isoformat(),
            "systems": self._get_city_transit_systems(city_name),
            "ridership": self._get_mock_ridership_data(city_name),
            "delays": [],
            "source": "Mock Data"
        }
    
    def _get_mock_bike_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Return mock bike share data"""
        return {
            "location": {"lat": lat, "lon": lon},
            "timestamp": datetime.utcnow().isoformat(),
            "stations": self._get_mock_bike_stations(lat, lon),
            "total_bikes": 120,
            "total_docks": 180,
            "utilization_rate": 0.67,
            "source": "Mock Data"
        }
    
    def _get_mock_emissions_data(self, city_name: str) -> Dict[str, Any]:
        """Return mock emissions data"""
        return {
            "city": city_name,
            "timestamp": datetime.utcnow().isoformat(),
            "total_transportation_emissions": self._get_city_emissions(city_name),
            "emissions_by_mode": {
                "private_vehicles": 0.65,
                "public_transit": 0.15,
                "commercial_vehicles": 0.15,
                "aviation": 0.05
            },
            "emissions_trends": self._get_emissions_trends(),
            "source": "Mock Data"
        }

# Global instance
transportation_service = TransportationService()
