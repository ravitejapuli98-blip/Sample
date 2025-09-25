"""
City data models for mobility, air quality, and energy data
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class City(Base):
    """City entity"""
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False, default="USA")
    population = Column(Integer)
    area_km2 = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String(50))
    
    # Relationships
    mobility_data = relationship("MobilityData", back_populates="city")
    air_quality_data = relationship("AirQualityData", back_populates="city")
    energy_data = relationship("EnergyData", back_populates="city")
    policies = relationship("Policy", back_populates="city")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MobilityData(Base):
    """Mobility and transportation data"""
    __tablename__ = "mobility_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    
    # Traffic data
    avg_travel_time_minutes = Column(Float)
    congestion_level = Column(Float)  # 0-1 scale
    vehicle_count = Column(Integer)
    public_transit_ridership = Column(Integer)
    
    # Infrastructure
    road_length_km = Column(Float)
    bike_lane_length_km = Column(Float)
    bus_stops_count = Column(Integer)
    ev_charging_stations = Column(Integer)
    
    # Modal split
    car_share = Column(Float)  # percentage
    public_transit_share = Column(Float)
    bike_share = Column(Float)
    walk_share = Column(Float)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    city = relationship("City", back_populates="mobility_data")


class AirQualityData(Base):
    """Air quality monitoring data"""
    __tablename__ = "air_quality_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    
    # Air quality metrics
    pm25_ug_m3 = Column(Float)  # PM2.5 in μg/m³
    pm10_ug_m3 = Column(Float)  # PM10 in μg/m³
    no2_ppb = Column(Float)     # NO2 in ppb
    o3_ppb = Column(Float)      # O3 in ppb
    co_ppm = Column(Float)      # CO in ppm
    so2_ppb = Column(Float)     # SO2 in ppb
    
    # Air quality index
    aqi = Column(Integer)
    aqi_category = Column(String(20))  # Good, Moderate, Unhealthy, etc.
    
    # Weather conditions
    temperature_c = Column(Float)
    humidity_percent = Column(Float)
    wind_speed_mps = Column(Float)
    wind_direction_deg = Column(Float)
    
    # Location
    station_latitude = Column(Float)
    station_longitude = Column(Float)
    station_name = Column(String(100))
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    city = relationship("City", back_populates="air_quality_data")


class EnergyData(Base):
    """Energy consumption and grid data"""
    __tablename__ = "energy_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    
    # Energy consumption
    total_consumption_mwh = Column(Float)
    residential_consumption_mwh = Column(Float)
    commercial_consumption_mwh = Column(Float)
    industrial_consumption_mwh = Column(Float)
    transportation_consumption_mwh = Column(Float)
    
    # Renewable energy
    solar_generation_mwh = Column(Float)
    wind_generation_mwh = Column(Float)
    hydro_generation_mwh = Column(Float)
    renewable_percentage = Column(Float)
    
    # Grid metrics
    peak_demand_mw = Column(Float)
    grid_efficiency = Column(Float)  # 0-1 scale
    power_outages_count = Column(Integer)
    avg_outage_duration_minutes = Column(Float)
    
    # EV infrastructure
    ev_charging_demand_mw = Column(Float)
    ev_penetration_rate = Column(Float)  # percentage
    
    # Carbon intensity
    co2_emissions_kg_mwh = Column(Float)
    total_co2_emissions_tonnes = Column(Float)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    city = relationship("City", back_populates="energy_data")


class Neighborhood(Base):
    """Neighborhood-level data for equity analysis"""
    __tablename__ = "neighborhoods"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    
    name = Column(String(100), nullable=False)
    population = Column(Integer)
    area_km2 = Column(Float)
    
    # Demographics
    median_income = Column(Float)
    poverty_rate = Column(Float)
    education_level = Column(Float)  # percentage with college degree
    
    # Transportation access
    transit_accessibility_score = Column(Float)  # 0-1 scale
    walkability_score = Column(Float)  # 0-1 scale
    bike_infrastructure_score = Column(Float)  # 0-1 scale
    
    # Environmental justice
    environmental_burden_score = Column(Float)  # 0-1 scale
    air_quality_exposure = Column(Float)
    heat_island_effect = Column(Float)
    
    # Geographic bounds
    bounds_geojson = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
