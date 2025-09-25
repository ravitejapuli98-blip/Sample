"""
Policy models for sustainable urban planning
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Policy(Base):
    """Policy entity"""
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # transportation, energy, air_quality, etc.
    policy_type = Column(String(50), nullable=False)  # infrastructure, regulation, incentive, etc.
    
    # Policy parameters
    parameters = Column(JSON)  # Flexible JSON for policy-specific parameters
    
    # Implementation details
    implementation_cost = Column(Float)  # in USD
    implementation_timeline_months = Column(Integer)
    maintenance_cost_annual = Column(Float)
    
    # Status
    status = Column(String(20), default="draft")  # draft, active, completed, cancelled
    priority = Column(Integer, default=1)  # 1-5 scale
    
    # Relationships
    city = relationship("City", back_populates="policies")
    policy_components = relationship("PolicyComponent", back_populates="policy")
    simulations = relationship("Simulation", back_populates="policy")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PolicyComponent(Base):
    """Individual components of a policy package"""
    __tablename__ = "policy_components"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    
    name = Column(String(200), nullable=False)
    component_type = Column(String(50), nullable=False)  # bus_lane, ev_charging, signal_timing, etc.
    description = Column(Text)
    
    # Component parameters
    parameters = Column(JSON)
    
    # Geographic scope
    affected_area_geojson = Column(JSON)
    affected_neighborhoods = Column(JSON)  # List of neighborhood IDs
    
    # Implementation details
    cost = Column(Float)
    timeline_months = Column(Integer)
    
    # Relationships
    policy = relationship("Policy", back_populates="policy_components")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PolicyPackage(Base):
    """Collection of policies that work together"""
    __tablename__ = "policy_packages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Package metadata
    total_cost = Column(Float)
    implementation_timeline_months = Column(Integer)
    expected_benefits = Column(JSON)
    
    # Status
    status = Column(String(20), default="draft")
    
    # Relationships
    package_policies = relationship("PackagePolicy", back_populates="policy_package")
    simulations = relationship("Simulation", back_populates="policy_package")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PackagePolicy(Base):
    """Many-to-many relationship between packages and policies"""
    __tablename__ = "package_policies"
    
    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("policy_packages.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    
    # Implementation order and timing
    implementation_order = Column(Integer)
    start_month = Column(Integer)  # Month within package timeline
    
    # Relationships
    policy_package = relationship("PolicyPackage", back_populates="package_policies")
    policy = relationship("Policy")


class PolicyOutcome(Base):
    """Predicted outcomes of policy implementations"""
    __tablename__ = "policy_outcomes"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    
    # Environmental outcomes
    co2_reduction_tonnes = Column(Float)
    pm25_reduction_ug_m3 = Column(Float)
    energy_savings_mwh = Column(Float)
    
    # Transportation outcomes
    travel_time_reduction_minutes = Column(Float)
    congestion_reduction_percent = Column(Float)
    modal_shift_percent = Column(JSON)  # {car: -5, transit: +10, bike: +3, walk: +2}
    
    # Economic outcomes
    cost_benefit_ratio = Column(Float)
    roi_percent = Column(Float)
    job_creation_count = Column(Integer)
    
    # Equity outcomes
    equity_score = Column(Float)  # 0-1 scale
    low_income_benefit_percent = Column(Float)
    accessibility_improvement_percent = Column(Float)
    
    # Health outcomes
    health_benefits_annual = Column(Float)  # in USD
    premature_deaths_averted = Column(Float)
    
    # Confidence and uncertainty
    confidence_score = Column(Float)  # 0-1 scale
    uncertainty_bounds = Column(JSON)  # {lower: {...}, upper: {...}}
    
    # Time horizon
    time_horizon_years = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PolicyRecommendation(Base):
    """AI-generated policy recommendations"""
    __tablename__ = "policy_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    
    # Recommendation details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    rationale = Column(Text)
    
    # Recommendation type
    recommendation_type = Column(String(50))  # quick_win, long_term, emergency, etc.
    priority_score = Column(Float)  # 0-1 scale
    
    # Expected outcomes
    expected_outcomes = Column(JSON)
    confidence_score = Column(Float)
    
    # Implementation details
    estimated_cost = Column(Float)
    implementation_difficulty = Column(String(20))  # low, medium, high
    timeline_months = Column(Integer)
    
    # Status
    status = Column(String(20), default="generated")  # generated, reviewed, accepted, rejected
    
    # Relationships
    city = relationship("City")
    recommended_policies = relationship("RecommendationPolicy", back_populates="recommendation")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RecommendationPolicy(Base):
    """Policies included in a recommendation"""
    __tablename__ = "recommendation_policies"
    
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("policy_recommendations.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    
    # Relationship details
    importance_weight = Column(Float)  # 0-1 scale
    implementation_order = Column(Integer)
    
    # Relationships
    recommendation = relationship("PolicyRecommendation", back_populates="recommended_policies")
    policy = relationship("Policy")
