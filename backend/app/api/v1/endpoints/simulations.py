"""
Simulation endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.simulation import Simulation, SimulationRun
from app.models.policy import Policy, PolicyPackage
from app.models.city import City
from app.schemas.simulation import (
    SimulationCreate, SimulationUpdate, SimulationResponse,
    SimulationRunResponse
)
from app.simulation.engine import SimulationEngine

router = APIRouter()


@router.get("/", response_model=List[SimulationResponse])
async def get_simulations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    city_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of simulations"""
    query = db.query(Simulation)
    
    if city_id:
        query = query.filter(Simulation.city_id == city_id)
    if status:
        query = query.filter(Simulation.status == status)
    
    simulations = query.offset(skip).limit(limit).all()
    return simulations


@router.get("/{simulation_id}", response_model=SimulationResponse)
async def get_simulation(simulation_id: int, db: Session = Depends(get_db)):
    """Get simulation by ID"""
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return simulation


@router.post("/", response_model=SimulationResponse)
async def create_simulation(simulation: SimulationCreate, db: Session = Depends(get_db)):
    """Create a new simulation"""
    # Verify city exists
    city = db.query(City).filter(City.id == simulation.city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Verify policy exists if specified
    if simulation.policy_id:
        policy = db.query(Policy).filter(Policy.id == simulation.policy_id).first()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
    
    # Verify policy package exists if specified
    if simulation.policy_package_id:
        package = db.query(PolicyPackage).filter(PolicyPackage.id == simulation.policy_package_id).first()
        if not package:
            raise HTTPException(status_code=404, detail="Policy package not found")
    
    db_simulation = Simulation(**simulation.dict())
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    return db_simulation


@router.post("/{simulation_id}/run")
async def run_simulation(
    simulation_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Run a simulation"""
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    if simulation.status == "running":
        raise HTTPException(status_code=400, detail="Simulation is already running")
    
    # Update simulation status
    simulation.status = "running"
    simulation.progress_percent = 0.0
    db.commit()
    
    # Start simulation in background
    background_tasks.add_task(_run_simulation_task, simulation_id, db)
    
    return {"message": "Simulation started", "simulation_id": simulation_id}


@router.get("/{simulation_id}/runs", response_model=List[SimulationRunResponse])
async def get_simulation_runs(
    simulation_id: int,
    db: Session = Depends(get_db)
):
    """Get simulation runs for a simulation"""
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    runs = db.query(SimulationRun).filter(
        SimulationRun.simulation_id == simulation_id
    ).order_by(SimulationRun.created_at.desc()).all()
    return runs


@router.get("/{simulation_id}/results")
async def get_simulation_results(simulation_id: int, db: Session = Depends(get_db)):
    """Get simulation results"""
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    if simulation.status != "completed":
        raise HTTPException(status_code=400, detail="Simulation not completed")
    
    return {
        "simulation_id": simulation_id,
        "results": simulation.results,
        "metrics": simulation.metrics,
        "status": simulation.status,
        "progress_percent": simulation.progress_percent
    }


async def _run_simulation_task(simulation_id: int, db: Session):
    """Background task to run simulation"""
    try:
        # Get simulation
        simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if not simulation:
            return
        
        # Get city and policies
        city = db.query(City).filter(City.id == simulation.city_id).first()
        policies = []
        
        if simulation.policy_id:
            policy = db.query(Policy).filter(Policy.id == simulation.policy_id).first()
            if policy:
                policies = [policy]
        
        # Initialize simulation engine
        engine = SimulationEngine()
        await engine.initialize_simulation(
            city, policies, simulation.agent_count
        )
        
        # Run simulation
        results = await engine.run_simulation(simulation.timesteps)
        
        # Update simulation with results
        simulation.results = results
        simulation.metrics = {
            'total_agents': len(engine.agents),
            'total_timesteps': simulation.timesteps,
            'total_co2_emissions': results.get('total_co2_emissions', 0),
            'total_energy_consumption': results.get('total_energy_consumption', 0),
            'avg_travel_time': results.get('avg_travel_time', 0),
            'modal_split': results.get('modal_split', {})
        }
        simulation.status = "completed"
        simulation.progress_percent = 100.0
        
        db.commit()
        
    except Exception as e:
        # Update simulation status to failed
        simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if simulation:
            simulation.status = "failed"
            simulation.results = {"error": str(e)}
            db.commit()
