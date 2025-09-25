"""
Simulation models for multi-agent urban planning simulations
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Simulation(Base):
    """Simulation entity"""
    __tablename__ = "simulations"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True)
    policy_package_id = Column(Integer, ForeignKey("policy_packages.id"), nullable=True)
    
    # Simulation metadata
    name = Column(String(200), nullable=False)
    description = Column(Text)
    simulation_type = Column(String(50), nullable=False)  # policy_test, scenario_analysis, optimization
    
    # Simulation parameters
    parameters = Column(JSON)  # Simulation-specific parameters
    timesteps = Column(Integer, default=1000)
    agent_count = Column(Integer, default=1000)
    
    # Status and results
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    progress_percent = Column(Float, default=0.0)
    
    # Results
    results = Column(JSON)  # Simulation results
    metrics = Column(JSON)  # Key performance indicators
    
    # Relationships
    city = relationship("City")
    policy = relationship("Policy", back_populates="simulations")
    policy_package = relationship("PolicyPackage", back_populates="simulations")
    simulation_runs = relationship("SimulationRun", back_populates="simulation")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SimulationRun(Base):
    """Individual simulation run within a simulation"""
    __tablename__ = "simulation_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    
    # Run metadata
    run_number = Column(Integer, nullable=False)
    seed = Column(Integer)  # Random seed for reproducibility
    
    # Run parameters
    parameters = Column(JSON)  # Run-specific parameters
    
    # Status and timing
    status = Column(String(20), default="pending")
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)
    
    # Results
    results = Column(JSON)
    metrics = Column(JSON)
    agent_data = Column(JSON)  # Detailed agent behavior data
    
    # Relationships
    simulation = relationship("Simulation", back_populates="simulation_runs")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Agent(Base):
    """Agent entity for multi-agent simulations"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    simulation_run_id = Column(Integer, ForeignKey("simulation_runs.id"), nullable=False)
    
    # Agent identification
    agent_id = Column(String(50), nullable=False)  # Unique within simulation
    agent_type = Column(String(50), nullable=False)  # commuter, resident, business, etc.
    
    # Agent properties
    properties = Column(JSON)  # Agent-specific properties
    
    # Location and behavior
    home_location = Column(JSON)  # {lat, lng}
    work_location = Column(JSON)  # {lat, lng}
    activity_locations = Column(JSON)  # List of locations
    
    # Transportation preferences
    transport_mode_preferences = Column(JSON)  # {car: 0.6, transit: 0.3, bike: 0.1}
    vehicle_type = Column(String(20))  # gas, hybrid, electric, none
    
    # Socioeconomic factors
    income_level = Column(String(20))  # low, medium, high
    age_group = Column(String(20))  # young, adult, senior
    household_size = Column(Integer)
    
    # Relationships
    simulation_run = relationship("SimulationRun")
    agent_behaviors = relationship("AgentBehavior", back_populates="agent")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AgentBehavior(Base):
    """Agent behavior data during simulation"""
    __tablename__ = "agent_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    simulation_run_id = Column(Integer, ForeignKey("simulation_runs.id"), nullable=False)
    
    # Behavior data
    timestep = Column(Integer, nullable=False)
    location = Column(JSON)  # {lat, lng}
    activity = Column(String(50))  # home, work, shopping, recreation
    transport_mode = Column(String(20))  # car, transit, bike, walk
    
    # Travel data
    origin = Column(JSON)  # {lat, lng}
    destination = Column(JSON)  # {lat, lng}
    travel_time_minutes = Column(Float)
    distance_km = Column(Float)
    route = Column(JSON)  # List of waypoints
    
    # Environmental impact
    co2_emissions_kg = Column(Float)
    energy_consumption_kwh = Column(Float)
    
    # Relationships
    agent = relationship("Agent", back_populates="agent_behaviors")
    simulation_run = relationship("SimulationRun")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulationScenario(Base):
    """Predefined simulation scenarios"""
    __tablename__ = "simulation_scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Scenario parameters
    parameters = Column(JSON)
    
    # Baseline conditions
    baseline_conditions = Column(JSON)
    
    # Policy interventions
    policy_interventions = Column(JSON)
    
    # Expected outcomes
    expected_outcomes = Column(JSON)
    
    # Status
    status = Column(String(20), default="draft")  # draft, active, archived
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SimulationTemplate(Base):
    """Reusable simulation templates"""
    __tablename__ = "simulation_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # transportation, energy, air_quality, etc.
    
    # Template configuration
    template_config = Column(JSON)
    
    # Default parameters
    default_parameters = Column(JSON)
    
    # Agent configurations
    agent_configs = Column(JSON)
    
    # Environment setup
    environment_config = Column(JSON)
    
    # Status
    status = Column(String(20), default="draft")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
