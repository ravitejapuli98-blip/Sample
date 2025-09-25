"""
City data endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.city import City, MobilityData, AirQualityData, EnergyData, Neighborhood
from app.schemas.city import (
    CityCreate, CityUpdate, CityResponse,
    MobilityDataCreate, MobilityDataResponse,
    AirQualityDataCreate, AirQualityDataResponse,
    EnergyDataCreate, EnergyDataResponse,
    NeighborhoodResponse
)

router = APIRouter()


@router.get("/", response_model=List[CityResponse])
async def get_cities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of cities"""
    query = db.query(City)
    
    if search:
        query = query.filter(City.name.ilike(f"%{search}%"))
    
    cities = query.offset(skip).limit(limit).all()
    return cities


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(city_id: int, db: Session = Depends(get_db)):
    """Get city by ID"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/", response_model=CityResponse)
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
    """Create a new city"""
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.put("/{city_id}", response_model=CityResponse)
async def update_city(
    city_id: int, 
    city_update: CityUpdate, 
    db: Session = Depends(get_db)
):
    """Update city information"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    for field, value in city_update.dict(exclude_unset=True).items():
        setattr(city, field, value)
    
    db.commit()
    db.refresh(city)
    return city


@router.delete("/{city_id}")
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Delete a city"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    db.delete(city)
    db.commit()
    return {"message": "City deleted successfully"}


@router.get("/{city_id}/mobility", response_model=List[MobilityDataResponse])
async def get_mobility_data(
    city_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get mobility data for a city"""
    query = db.query(MobilityData).filter(MobilityData.city_id == city_id)
    
    if start_date:
        query = query.filter(MobilityData.timestamp >= start_date)
    if end_date:
        query = query.filter(MobilityData.timestamp <= end_date)
    
    mobility_data = query.order_by(MobilityData.timestamp.desc()).limit(limit).all()
    return mobility_data


@router.post("/{city_id}/mobility", response_model=MobilityDataResponse)
async def create_mobility_data(
    city_id: int,
    mobility_data: MobilityDataCreate,
    db: Session = Depends(get_db)
):
    """Create mobility data for a city"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    db_mobility_data = MobilityData(city_id=city_id, **mobility_data.dict())
    db.add(db_mobility_data)
    db.commit()
    db.refresh(db_mobility_data)
    return db_mobility_data


@router.get("/{city_id}/air-quality", response_model=List[AirQualityDataResponse])
async def get_air_quality_data(
    city_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get air quality data for a city"""
    query = db.query(AirQualityData).filter(AirQualityData.city_id == city_id)
    
    if start_date:
        query = query.filter(AirQualityData.timestamp >= start_date)
    if end_date:
        query = query.filter(AirQualityData.timestamp <= end_date)
    
    air_quality_data = query.order_by(AirQualityData.timestamp.desc()).limit(limit).all()
    return air_quality_data


@router.post("/{city_id}/air-quality", response_model=AirQualityDataResponse)
async def create_air_quality_data(
    city_id: int,
    air_quality_data: AirQualityDataCreate,
    db: Session = Depends(get_db)
):
    """Create air quality data for a city"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    db_air_quality_data = AirQualityData(city_id=city_id, **air_quality_data.dict())
    db.add(db_air_quality_data)
    db.commit()
    db.refresh(db_air_quality_data)
    return db_air_quality_data


@router.get("/{city_id}/energy", response_model=List[EnergyDataResponse])
async def get_energy_data(
    city_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get energy data for a city"""
    query = db.query(EnergyData).filter(EnergyData.city_id == city_id)
    
    if start_date:
        query = query.filter(EnergyData.timestamp >= start_date)
    if end_date:
        query = query.filter(EnergyData.timestamp <= end_date)
    
    energy_data = query.order_by(EnergyData.timestamp.desc()).limit(limit).all()
    return energy_data


@router.post("/{city_id}/energy", response_model=EnergyDataResponse)
async def create_energy_data(
    city_id: int,
    energy_data: EnergyDataCreate,
    db: Session = Depends(get_db)
):
    """Create energy data for a city"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    db_energy_data = EnergyData(city_id=city_id, **energy_data.dict())
    db.add(db_energy_data)
    db.commit()
    db.refresh(db_energy_data)
    return db_energy_data


@router.get("/{city_id}/neighborhoods", response_model=List[NeighborhoodResponse])
async def get_neighborhoods(city_id: int, db: Session = Depends(get_db)):
    """Get neighborhoods for a city"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    neighborhoods = db.query(Neighborhood).filter(Neighborhood.city_id == city_id).all()
    return neighborhoods


@router.get("/{city_id}/dashboard")
async def get_city_dashboard(city_id: int, db: Session = Depends(get_db)):
    """Get comprehensive dashboard data for a city"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Get latest data from each category
    latest_mobility = db.query(MobilityData).filter(
        MobilityData.city_id == city_id
    ).order_by(MobilityData.timestamp.desc()).first()
    
    latest_air_quality = db.query(AirQualityData).filter(
        AirQualityData.city_id == city_id
    ).order_by(AirQualityData.timestamp.desc()).first()
    
    latest_energy = db.query(EnergyData).filter(
        EnergyData.city_id == city_id
    ).order_by(EnergyData.timestamp.desc()).first()
    
    neighborhoods = db.query(Neighborhood).filter(
        Neighborhood.city_id == city_id
    ).all()
    
    return {
        "city": city,
        "latest_mobility": latest_mobility,
        "latest_air_quality": latest_air_quality,
        "latest_energy": latest_energy,
        "neighborhoods": neighborhoods,
        "summary": {
            "total_neighborhoods": len(neighborhoods),
            "avg_travel_time": latest_mobility.avg_travel_time_minutes if latest_mobility else None,
            "air_quality_index": latest_air_quality.aqi if latest_air_quality else None,
            "renewable_percentage": latest_energy.renewable_percentage if latest_energy else None
        }
    }
