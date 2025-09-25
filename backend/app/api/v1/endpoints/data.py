"""
Data ingestion and management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import json
from datetime import datetime

from app.core.database import get_db
from app.models.city import City, MobilityData, AirQualityData, EnergyData
from app.schemas.city import (
    MobilityDataCreate, AirQualityDataCreate, EnergyDataCreate
)

router = APIRouter()


@router.post("/upload/mobility/{city_id}")
async def upload_mobility_data(
    city_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Upload mobility data from CSV file"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(contents.decode('utf-8'))
        
        # Validate required columns
        required_columns = ['timestamp', 'avg_travel_time_minutes', 'congestion_level']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing_columns}"
            )
        
        # Process and save data
        records_created = 0
        for _, row in df.iterrows():
            mobility_data = MobilityDataCreate(
                avg_travel_time_minutes=row.get('avg_travel_time_minutes'),
                congestion_level=row.get('congestion_level'),
                vehicle_count=row.get('vehicle_count'),
                public_transit_ridership=row.get('public_transit_ridership'),
                road_length_km=row.get('road_length_km'),
                bike_lane_length_km=row.get('bike_lane_length_km'),
                bus_stops_count=row.get('bus_stops_count'),
                ev_charging_stations=row.get('ev_charging_stations'),
                car_share=row.get('car_share'),
                public_transit_share=row.get('public_transit_share'),
                bike_share=row.get('bike_share'),
                walk_share=row.get('walk_share')
            )
            
            db_mobility_data = MobilityData(
                city_id=city_id,
                timestamp=pd.to_datetime(row['timestamp']),
                **mobility_data.dict(exclude_none=True)
            )
            db.add(db_mobility_data)
            records_created += 1
        
        db.commit()
        
        return {
            "message": f"Successfully uploaded {records_created} mobility data records",
            "city_id": city_id,
            "records_created": records_created
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


@router.post("/upload/air-quality/{city_id}")
async def upload_air_quality_data(
    city_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Upload air quality data from CSV file"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(contents.decode('utf-8'))
        
        # Validate required columns
        required_columns = ['timestamp', 'pm25_ug_m3', 'aqi']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing_columns}"
            )
        
        # Process and save data
        records_created = 0
        for _, row in df.iterrows():
            air_quality_data = AirQualityDataCreate(
                pm25_ug_m3=row.get('pm25_ug_m3'),
                pm10_ug_m3=row.get('pm10_ug_m3'),
                no2_ppb=row.get('no2_ppb'),
                o3_ppb=row.get('o3_ppb'),
                co_ppm=row.get('co_ppm'),
                so2_ppb=row.get('so2_ppb'),
                aqi=row.get('aqi'),
                aqi_category=row.get('aqi_category'),
                temperature_c=row.get('temperature_c'),
                humidity_percent=row.get('humidity_percent'),
                wind_speed_mps=row.get('wind_speed_mps'),
                wind_direction_deg=row.get('wind_direction_deg'),
                station_latitude=row.get('station_latitude'),
                station_longitude=row.get('station_longitude'),
                station_name=row.get('station_name')
            )
            
            db_air_quality_data = AirQualityData(
                city_id=city_id,
                timestamp=pd.to_datetime(row['timestamp']),
                **air_quality_data.dict(exclude_none=True)
            )
            db.add(db_air_quality_data)
            records_created += 1
        
        db.commit()
        
        return {
            "message": f"Successfully uploaded {records_created} air quality data records",
            "city_id": city_id,
            "records_created": records_created
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


@router.post("/upload/energy/{city_id}")
async def upload_energy_data(
    city_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Upload energy data from CSV file"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(contents.decode('utf-8'))
        
        # Validate required columns
        required_columns = ['timestamp', 'total_consumption_mwh']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing_columns}"
            )
        
        # Process and save data
        records_created = 0
        for _, row in df.iterrows():
            energy_data = EnergyDataCreate(
                total_consumption_mwh=row.get('total_consumption_mwh'),
                residential_consumption_mwh=row.get('residential_consumption_mwh'),
                commercial_consumption_mwh=row.get('commercial_consumption_mwh'),
                industrial_consumption_mwh=row.get('industrial_consumption_mwh'),
                transportation_consumption_mwh=row.get('transportation_consumption_mwh'),
                solar_generation_mwh=row.get('solar_generation_mwh'),
                wind_generation_mwh=row.get('wind_generation_mwh'),
                hydro_generation_mwh=row.get('hydro_generation_mwh'),
                renewable_percentage=row.get('renewable_percentage'),
                peak_demand_mw=row.get('peak_demand_mw'),
                grid_efficiency=row.get('grid_efficiency'),
                power_outages_count=row.get('power_outages_count'),
                avg_outage_duration_minutes=row.get('avg_outage_duration_minutes'),
                ev_charging_demand_mw=row.get('ev_charging_demand_mw'),
                ev_penetration_rate=row.get('ev_penetration_rate'),
                co2_emissions_kg_mwh=row.get('co2_emissions_kg_mwh'),
                total_co2_emissions_tonnes=row.get('total_co2_emissions_tonnes')
            )
            
            db_energy_data = EnergyData(
                city_id=city_id,
                timestamp=pd.to_datetime(row['timestamp']),
                **energy_data.dict(exclude_none=True)
            )
            db.add(db_energy_data)
            records_created += 1
        
        db.commit()
        
        return {
            "message": f"Successfully uploaded {records_created} energy data records",
            "city_id": city_id,
            "records_created": records_created
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


@router.get("/export/{city_id}")
async def export_city_data(
    city_id: int,
    data_type: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Export city data as CSV"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    if data_type == "mobility":
        query = db.query(MobilityData).filter(MobilityData.city_id == city_id)
        if start_date:
            query = query.filter(MobilityData.timestamp >= start_date)
        if end_date:
            query = query.filter(MobilityData.timestamp <= end_date)
        
        data = query.all()
        df = pd.DataFrame([record.__dict__ for record in data])
        
    elif data_type == "air-quality":
        query = db.query(AirQualityData).filter(AirQualityData.city_id == city_id)
        if start_date:
            query = query.filter(AirQualityData.timestamp >= start_date)
        if end_date:
            query = query.filter(AirQualityData.timestamp <= end_date)
        
        data = query.all()
        df = pd.DataFrame([record.__dict__ for record in data])
        
    elif data_type == "energy":
        query = db.query(EnergyData).filter(EnergyData.city_id == city_id)
        if start_date:
            query = query.filter(EnergyData.timestamp >= start_date)
        if end_date:
            query = query.filter(EnergyData.timestamp <= end_date)
        
        data = query.all()
        df = pd.DataFrame([record.__dict__ for record in data])
        
    else:
        raise HTTPException(status_code=400, detail="Invalid data type")
    
    # Convert to CSV
    csv_content = df.to_csv(index=False)
    
    return {
        "message": f"Exported {len(data)} {data_type} records",
        "city_id": city_id,
        "data_type": data_type,
        "record_count": len(data),
        "csv_content": csv_content
    }
