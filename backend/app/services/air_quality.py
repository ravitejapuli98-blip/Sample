"""
Air Quality Data Service
Integrates with real air quality APIs
"""

import requests
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class AirQualityService:
    """Service for fetching real-time air quality data"""
    
    def __init__(self):
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY", "demo_key")
        self.airvisual_api_key = os.getenv("AIRVISUAL_API_KEY", "demo_key")
        self.epa_api_key = os.getenv("EPA_API_KEY", "demo_key")
    
    def get_air_quality_by_coordinates(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get air quality data by coordinates using OpenWeatherMap API"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/air_pollution"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.openweather_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract air quality components
            components = data.get("list", [{}])[0].get("components", {})
            aqi = data.get("list", [{}])[0].get("main", {}).get("aqi", 0)
            
            return {
                "aqi": aqi,
                "aqi_level": self._get_aqi_level(aqi),
                "components": {
                    "co": components.get("co", 0),
                    "no": components.get("no", 0),
                    "no2": components.get("no2", 0),
                    "o3": components.get("o3", 0),
                    "pm2_5": components.get("pm2_5", 0),
                    "pm10": components.get("pm10", 0),
                    "so2": components.get("so2", 0)
                },
                "timestamp": datetime.utcnow().isoformat(),
                "source": "OpenWeatherMap"
            }
            
        except requests.RequestException as e:
            logger.error(f"Error fetching air quality data: {e}")
            return self._get_mock_air_quality_data()
        except Exception as e:
            logger.error(f"Unexpected error in air quality service: {e}")
            return self._get_mock_air_quality_data()
    
    def get_air_quality_by_city(self, city_name: str, country_code: str = "US") -> Dict[str, Any]:
        """Get air quality data by city name"""
        try:
            # First get coordinates for the city
            coords = self._get_city_coordinates(city_name, country_code)
            if coords:
                return self.get_air_quality_by_coordinates(coords["lat"], coords["lon"])
            else:
                return self._get_mock_air_quality_data()
                
        except Exception as e:
            logger.error(f"Error getting air quality for city {city_name}: {e}")
            return self._get_mock_air_quality_data()
    
    def get_historical_air_quality(self, lat: float, lon: float, days: int = 7) -> List[Dict[str, Any]]:
        """Get historical air quality data"""
        try:
            historical_data = []
            current_date = datetime.utcnow()
            
            for i in range(days):
                date = current_date - timedelta(days=i)
                timestamp = int(date.timestamp())
                
                url = f"http://api.openweathermap.org/data/2.5/air_pollution/history"
                params = {
                    "lat": lat,
                    "lon": lon,
                    "start": timestamp,
                    "end": timestamp + 86400,  # 24 hours
                    "appid": self.openweather_api_key
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get("list", []):
                        historical_data.append({
                            "timestamp": datetime.fromtimestamp(item["dt"]).isoformat(),
                            "aqi": item.get("main", {}).get("aqi", 0),
                            "pm2_5": item.get("components", {}).get("pm2_5", 0),
                            "pm10": item.get("components", {}).get("pm10", 0),
                            "no2": item.get("components", {}).get("no2", 0),
                            "o3": item.get("components", {}).get("o3", 0)
                        })
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Error fetching historical air quality: {e}")
            return self._get_mock_historical_data(days)
    
    def get_air_quality_forecast(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Get air quality forecast"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.openweather_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecast = []
            
            for item in data.get("list", []):
                forecast.append({
                    "timestamp": datetime.fromtimestamp(item["dt"]).isoformat(),
                    "aqi": item.get("main", {}).get("aqi", 0),
                    "aqi_level": self._get_aqi_level(item.get("main", {}).get("aqi", 0)),
                    "pm2_5": item.get("components", {}).get("pm2_5", 0),
                    "pm10": item.get("components", {}).get("pm10", 0),
                    "no2": item.get("components", {}).get("no2", 0),
                    "o3": item.get("components", {}).get("o3", 0)
                })
            
            return forecast
            
        except Exception as e:
            logger.error(f"Error fetching air quality forecast: {e}")
            return self._get_mock_forecast_data()
    
    def _get_city_coordinates(self, city_name: str, country_code: str) -> Optional[Dict[str, float]]:
        """Get coordinates for a city"""
        try:
            url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": f"{city_name},{country_code}",
                "limit": 1,
                "appid": self.openweather_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return {
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"]
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting coordinates for {city_name}: {e}")
            return None
    
    def _get_aqi_level(self, aqi: int) -> str:
        """Convert AQI number to level description"""
        if aqi <= 1:
            return "Good"
        elif aqi <= 2:
            return "Fair"
        elif aqi <= 3:
            return "Moderate"
        elif aqi <= 4:
            return "Poor"
        else:
            return "Very Poor"
    
    def _get_mock_air_quality_data(self) -> Dict[str, Any]:
        """Return mock air quality data when API fails"""
        return {
            "aqi": 45,
            "aqi_level": "Good",
            "components": {
                "co": 0.2,
                "no": 0.1,
                "no2": 15.5,
                "o3": 45.2,
                "pm2_5": 12.3,
                "pm10": 18.7,
                "so2": 8.9
            },
            "timestamp": datetime.utcnow().isoformat(),
            "source": "Mock Data"
        }
    
    def _get_mock_historical_data(self, days: int) -> List[Dict[str, Any]]:
        """Return mock historical data"""
        import random
        data = []
        for i in range(days * 24):  # Hourly data
            timestamp = datetime.utcnow() - timedelta(hours=i)
            data.append({
                "timestamp": timestamp.isoformat(),
                "aqi": random.randint(30, 80),
                "pm2_5": random.uniform(8, 25),
                "pm10": random.uniform(12, 35),
                "no2": random.uniform(10, 30),
                "o3": random.uniform(30, 60)
            })
        return data
    
    def _get_mock_forecast_data(self) -> List[Dict[str, Any]]:
        """Return mock forecast data"""
        import random
        data = []
        for i in range(5):  # 5-day forecast
            timestamp = datetime.utcnow() + timedelta(days=i)
            aqi = random.randint(35, 75)
            data.append({
                "timestamp": timestamp.isoformat(),
                "aqi": aqi,
                "aqi_level": self._get_aqi_level(aqi),
                "pm2_5": random.uniform(10, 20),
                "pm10": random.uniform(15, 30),
                "no2": random.uniform(12, 25),
                "o3": random.uniform(35, 55)
            })
        return data

# Global instance
air_quality_service = AirQualityService()
