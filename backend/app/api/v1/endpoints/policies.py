"""
Policy endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.policy import Policy, PolicyComponent, PolicyPackage, PolicyRecommendation
from app.models.city import City
from app.schemas.policy import (
    PolicyCreate, PolicyUpdate, PolicyResponse,
    PolicyComponentCreate, PolicyComponentResponse,
    PolicyPackageCreate, PolicyPackageResponse,
    PolicyRecommendationResponse,
    PolicyConstraint
)
from app.policy.engine import PolicyRecommendationEngine, PolicyOptimizationEngine

router = APIRouter()


@router.get("/", response_model=List[PolicyResponse])
async def get_policies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    city_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of policies"""
    query = db.query(Policy)
    
    if city_id:
        query = query.filter(Policy.city_id == city_id)
    if category:
        query = query.filter(Policy.category == category)
    if status:
        query = query.filter(Policy.status == status)
    
    policies = query.offset(skip).limit(limit).all()
    return policies


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(policy_id: int, db: Session = Depends(get_db)):
    """Get policy by ID"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.post("/", response_model=PolicyResponse)
async def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    """Create a new policy"""
    # Verify city exists
    city = db.query(City).filter(City.id == policy.city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    db_policy = Policy(**policy.dict())
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy


@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: int, 
    policy_update: PolicyUpdate, 
    db: Session = Depends(get_db)
):
    """Update policy information"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    for field, value in policy_update.dict(exclude_unset=True).items():
        setattr(policy, field, value)
    
    db.commit()
    db.refresh(policy)
    return policy


@router.delete("/{policy_id}")
async def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    """Delete a policy"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    db.delete(policy)
    db.commit()
    return {"message": "Policy deleted successfully"}


@router.get("/{policy_id}/components", response_model=List[PolicyComponentResponse])
async def get_policy_components(policy_id: int, db: Session = Depends(get_db)):
    """Get components of a policy"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    components = db.query(PolicyComponent).filter(
        PolicyComponent.policy_id == policy_id
    ).all()
    return components


@router.post("/{policy_id}/components", response_model=PolicyComponentResponse)
async def create_policy_component(
    policy_id: int,
    component: PolicyComponentCreate,
    db: Session = Depends(get_db)
):
    """Create a policy component"""
    # Verify policy exists
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    db_component = PolicyComponent(policy_id=policy_id, **component.dict())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component


@router.get("/packages/", response_model=List[PolicyPackageResponse])
async def get_policy_packages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of policy packages"""
    query = db.query(PolicyPackage)
    
    if status:
        query = query.filter(PolicyPackage.status == status)
    
    packages = query.offset(skip).limit(limit).all()
    return packages


@router.get("/packages/{package_id}", response_model=PolicyPackageResponse)
async def get_policy_package(package_id: int, db: Session = Depends(get_db)):
    """Get policy package by ID"""
    package = db.query(PolicyPackage).filter(PolicyPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Policy package not found")
    return package


@router.post("/packages/", response_model=PolicyPackageResponse)
async def create_policy_package(package: PolicyPackageCreate, db: Session = Depends(get_db)):
    """Create a new policy package"""
    db_package = PolicyPackage(**package.dict())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package


@router.post("/recommendations/{city_id}")
async def generate_policy_recommendations(
    city_id: int,
    constraints: PolicyConstraint,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate AI-powered policy recommendations for a city"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Get current city data
    current_data = await _get_city_current_data(city_id, db)
    
    # Generate recommendations
    recommendation_engine = PolicyRecommendationEngine()
    recommendations = await recommendation_engine.recommend_policies(
        city, constraints, current_data
    )
    
    # Save recommendations to database
    for recommendation in recommendations:
        db_recommendation = PolicyRecommendation(**recommendation.dict())
        db.add(db_recommendation)
    
    db.commit()
    
    return {
        "message": f"Generated {len(recommendations)} policy recommendations",
        "recommendations": recommendations
    }


@router.get("/recommendations/{city_id}", response_model=List[PolicyRecommendationResponse])
async def get_policy_recommendations(
    city_id: int,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get policy recommendations for a city"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    query = db.query(PolicyRecommendation).filter(
        PolicyRecommendation.city_id == city_id
    )
    
    if status:
        query = query.filter(PolicyRecommendation.status == status)
    
    recommendations = query.order_by(PolicyRecommendation.priority_score.desc()).all()
    return recommendations


@router.post("/optimize/{city_id}")
async def optimize_policy_package(
    city_id: int,
    constraints: PolicyConstraint,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Optimize a policy package for maximum impact"""
    # Verify city exists
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Get current city data
    current_data = await _get_city_current_data(city_id, db)
    
    # Optimize policy package
    optimization_engine = PolicyOptimizationEngine()
    optimized_package = await optimization_engine.optimize_policy_package(
        city, constraints, current_data
    )
    
    # Save optimized package to database
    db_package = PolicyPackage(**optimized_package.dict())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    
    return {
        "message": "Generated optimized policy package",
        "package": db_package
    }


async def _get_city_current_data(city_id: int, db: Session) -> dict:
    """Get current data for a city"""
    from app.models.city import MobilityData, AirQualityData, EnergyData
    
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
    
    return {
        'mobility_data': latest_mobility.__dict__ if latest_mobility else {},
        'air_quality_data': latest_air_quality.__dict__ if latest_air_quality else {},
        'energy_data': latest_energy.__dict__ if latest_energy else {}
    }
