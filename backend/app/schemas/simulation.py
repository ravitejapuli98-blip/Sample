"""
Pydantic schemas for simulation data
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SimulationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    simulation_type: str = Field(..., min_length=1, max_length=50)
    parameters: Optional[Dict[str, Any]] = None
    timesteps: int = Field(default=1000, ge=1)
    agent_count: int = Field(default=1000, ge=1)


class SimulationCreate(SimulationBase):
    city_id: int = Field(..., ge=1)
    policy_id: Optional[int] = Field(None, ge=1)
    policy_package_id: Optional[int] = Field(None, ge=1)


class SimulationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    simulation_type: Optional[str] = Field(None, min_length=1, max_length=50)
    parameters: Optional[Dict[str, Any]] = None
    timesteps: Optional[int] = Field(None, ge=1)
    agent_count: Optional[int] = Field(None, ge=1)
    status: Optional[str] = Field(None, max_length=20)


class SimulationResponse(SimulationBase):
    id: int
    city_id: int
    policy_id: Optional[int]
    policy_package_id: Optional[int]
    status: str
    progress_percent: float
    results: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class SimulationRunBase(BaseModel):
    run_number: int = Field(..., ge=1)
    seed: Optional[int] = None
    parameters: Optional[Dict[str, Any]] = None


class SimulationRunResponse(SimulationRunBase):
    id: int
    simulation_id: int
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    results: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
