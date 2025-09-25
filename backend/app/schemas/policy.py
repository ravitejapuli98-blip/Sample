"""
Pydantic schemas for policy data
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PolicyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=50)
    policy_type: str = Field(..., min_length=1, max_length=50)
    parameters: Optional[Dict[str, Any]] = None
    implementation_cost: Optional[float] = Field(None, ge=0)
    implementation_timeline_months: Optional[int] = Field(None, ge=1)
    maintenance_cost_annual: Optional[float] = Field(None, ge=0)
    priority: int = Field(default=1, ge=1, le=5)


class PolicyCreate(PolicyBase):
    city_id: int = Field(..., ge=1)


class PolicyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    policy_type: Optional[str] = Field(None, min_length=1, max_length=50)
    parameters: Optional[Dict[str, Any]] = None
    implementation_cost: Optional[float] = Field(None, ge=0)
    implementation_timeline_months: Optional[int] = Field(None, ge=1)
    maintenance_cost_annual: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=20)
    priority: Optional[int] = Field(None, ge=1, le=5)


class PolicyResponse(PolicyBase):
    id: int
    city_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PolicyComponentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    component_type: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    affected_area_geojson: Optional[Dict[str, Any]] = None
    affected_neighborhoods: Optional[List[int]] = None
    cost: Optional[float] = Field(None, ge=0)
    timeline_months: Optional[int] = Field(None, ge=1)


class PolicyComponentCreate(PolicyComponentBase):
    pass


class PolicyComponentResponse(PolicyComponentBase):
    id: int
    policy_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PolicyPackageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    total_cost: Optional[float] = Field(None, ge=0)
    implementation_timeline_months: Optional[int] = Field(None, ge=1)
    expected_benefits: Optional[Dict[str, Any]] = None


class PolicyPackageCreate(PolicyPackageBase):
    pass


class PolicyPackageResponse(PolicyPackageBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PolicyRecommendationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    rationale: Optional[str] = None
    recommendation_type: Optional[str] = Field(None, max_length=50)
    priority_score: Optional[float] = Field(None, ge=0, le=1)
    expected_outcomes: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    estimated_cost: Optional[float] = Field(None, ge=0)
    implementation_difficulty: Optional[str] = Field(None, max_length=20)
    timeline_months: Optional[int] = Field(None, ge=1)


class PolicyRecommendationResponse(PolicyRecommendationBase):
    id: int
    city_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PolicyConstraint(BaseModel):
    max_budget: float = Field(..., ge=0)
    max_timeline_months: int = Field(..., ge=1)
    min_equity_score: float = Field(default=0.0, ge=0, le=1)
    required_co2_reduction: float = Field(default=0.0, ge=0)
    excluded_policy_types: Optional[List[str]] = None


class PolicyOutcomeBase(BaseModel):
    co2_reduction_tonnes: Optional[float] = Field(None, ge=0)
    pm25_reduction_ug_m3: Optional[float] = Field(None, ge=0)
    travel_time_reduction_minutes: Optional[float] = Field(None, ge=0)
    energy_savings_mwh: Optional[float] = Field(None, ge=0)
    cost_benefit_ratio: Optional[float] = Field(None, ge=0)
    equity_score: Optional[float] = Field(None, ge=0, le=1)
    health_benefits_annual: Optional[float] = Field(None, ge=0)
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    time_horizon_years: Optional[int] = Field(None, ge=1)


class PolicyOutcomeResponse(PolicyOutcomeBase):
    id: int
    policy_id: int
    simulation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
