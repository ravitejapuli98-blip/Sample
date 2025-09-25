"""
Pydantic schemas for city data
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=50)
    country: str = Field(default="USA", max_length=50)
    population: Optional[int] = Field(None, ge=0)
    area_km2: Optional[float] = Field(None, ge=0)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    timezone: Optional[str] = Field(None, max_length=50)


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    population: Optional[int] = Field(None, ge=0)
    area_km2: Optional[float] = Field(None, ge=0)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    timezone: Optional[str] = Field(None, max_length=50)


class CityResponse(CityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class MobilityDataBase(BaseModel):
    avg_travel_time_minutes: Optional[float] = Field(None, ge=0)
    congestion_level: Optional[float] = Field(None, ge=0, le=1)
    vehicle_count: Optional[int] = Field(None, ge=0)
    public_transit_ridership: Optional[int] = Field(None, ge=0)
    road_length_km: Optional[float] = Field(None, ge=0)
    bike_lane_length_km: Optional[float] = Field(None, ge=0)
    bus_stops_count: Optional[int] = Field(None, ge=0)
    ev_charging_stations: Optional[int] = Field(None, ge=0)
    car_share: Optional[float] = Field(None, ge=0, le=100)
    public_transit_share: Optional[float] = Field(None, ge=0, le=100)
    bike_share: Optional[float] = Field(None, ge=0, le=100)
    walk_share: Optional[float] = Field(None, ge=0, le=100)


class MobilityDataCreate(MobilityDataBase):
    pass


class MobilityDataResponse(MobilityDataBase):
    id: int
    city_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class AirQualityDataBase(BaseModel):
    pm25_ug_m3: Optional[float] = Field(None, ge=0)
    pm10_ug_m3: Optional[float] = Field(None, ge=0)
    no2_ppb: Optional[float] = Field(None, ge=0)
    o3_ppb: Optional[float] = Field(None, ge=0)
    co_ppm: Optional[float] = Field(None, ge=0)
    so2_ppb: Optional[float] = Field(None, ge=0)
    aqi: Optional[int] = Field(None, ge=0, le=500)
    aqi_category: Optional[str] = Field(None, max_length=20)
    temperature_c: Optional[float] = Field(None, ge=-50, le=60)
    humidity_percent: Optional[float] = Field(None, ge=0, le=100)
    wind_speed_mps: Optional[float] = Field(None, ge=0)
    wind_direction_deg: Optional[float] = Field(None, ge=0, le=360)
    station_latitude: Optional[float] = Field(None, ge=-90, le=90)
    station_longitude: Optional[float] = Field(None, ge=-180, le=180)
    station_name: Optional[str] = Field(None, max_length=100)


class AirQualityDataCreate(AirQualityDataBase):
    pass


class AirQualityDataResponse(AirQualityDataBase):
    id: int
    city_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class EnergyDataBase(BaseModel):
    total_consumption_mwh: Optional[float] = Field(None, ge=0)
    residential_consumption_mwh: Optional[float] = Field(None, ge=0)
    commercial_consumption_mwh: Optional[float] = Field(None, ge=0)
    industrial_consumption_mwh: Optional[float] = Field(None, ge=0)
    transportation_consumption_mwh: Optional[float] = Field(None, ge=0)
    solar_generation_mwh: Optional[float] = Field(None, ge=0)
    wind_generation_mwh: Optional[float] = Field(None, ge=0)
    hydro_generation_mwh: Optional[float] = Field(None, ge=0)
    renewable_percentage: Optional[float] = Field(None, ge=0, le=100)
    peak_demand_mw: Optional[float] = Field(None, ge=0)
    grid_efficiency: Optional[float] = Field(None, ge=0, le=1)
    power_outages_count: Optional[int] = Field(None, ge=0)
    avg_outage_duration_minutes: Optional[float] = Field(None, ge=0)
    ev_charging_demand_mw: Optional[float] = Field(None, ge=0)
    ev_penetration_rate: Optional[float] = Field(None, ge=0, le=100)
    co2_emissions_kg_mwh: Optional[float] = Field(None, ge=0)
    total_co2_emissions_tonnes: Optional[float] = Field(None, ge=0)


class EnergyDataCreate(EnergyDataBase):
    pass


class EnergyDataResponse(EnergyDataBase):
    id: int
    city_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class NeighborhoodBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    population: Optional[int] = Field(None, ge=0)
    area_km2: Optional[float] = Field(None, ge=0)
    median_income: Optional[float] = Field(None, ge=0)
    poverty_rate: Optional[float] = Field(None, ge=0, le=100)
    education_level: Optional[float] = Field(None, ge=0, le=100)
    transit_accessibility_score: Optional[float] = Field(None, ge=0, le=1)
    walkability_score: Optional[float] = Field(None, ge=0, le=1)
    bike_infrastructure_score: Optional[float] = Field(None, ge=0, le=1)
    environmental_burden_score: Optional[float] = Field(None, ge=0, le=1)
    air_quality_exposure: Optional[float] = Field(None, ge=0)
    heat_island_effect: Optional[float] = Field(None, ge=0)
    bounds_geojson: Optional[Dict[str, Any]] = None


class NeighborhoodResponse(NeighborhoodBase):
    id: int
    city_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
