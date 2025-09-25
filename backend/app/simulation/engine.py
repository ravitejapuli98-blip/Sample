"""
Multi-agent simulation engine for urban planning
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
import networkx as nx
from dataclasses import dataclass
from enum import Enum

from app.core.config import settings
from app.models.simulation import Simulation, SimulationRun, Agent, AgentBehavior
from app.models.city import City, MobilityData, AirQualityData, EnergyData
from app.models.policy import Policy, PolicyComponent

logger = logging.getLogger(__name__)


class AgentType(Enum):
    COMMUTER = "commuter"
    RESIDENT = "resident"
    BUSINESS = "business"
    DELIVERY = "delivery"
    EMERGENCY = "emergency"


class TransportMode(Enum):
    CAR = "car"
    TRANSIT = "transit"
    BIKE = "bike"
    WALK = "walk"
    EV = "ev"


@dataclass
class Location:
    lat: float
    lng: float
    name: Optional[str] = None


@dataclass
class Route:
    origin: Location
    destination: Location
    waypoints: List[Location]
    distance_km: float
    travel_time_minutes: float
    transport_mode: TransportMode


class UrbanAgent:
    """Individual agent in the urban simulation"""
    
    def __init__(self, agent_id: str, agent_type: AgentType, properties: Dict[str, Any]):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.properties = properties
        
        # Location properties
        self.home_location = properties.get('home_location')
        self.work_location = properties.get('work_location')
        self.activity_locations = properties.get('activity_locations', [])
        
        # Transportation preferences
        self.transport_preferences = properties.get('transport_preferences', {
            TransportMode.CAR: 0.6,
            TransportMode.TRANSIT: 0.3,
            TransportMode.BIKE: 0.1
        })
        
        # Socioeconomic factors
        self.income_level = properties.get('income_level', 'medium')
        self.age_group = properties.get('age_group', 'adult')
        self.household_size = properties.get('household_size', 2)
        
        # Current state
        self.current_location = self.home_location
        self.current_activity = 'home'
        self.current_route = None
        self.vehicle_type = properties.get('vehicle_type', 'gas')
        
        # Behavior history
        self.behavior_history = []
    
    def choose_transport_mode(self, route: Route, policy_impacts: Dict[str, Any]) -> TransportMode:
        """Choose transportation mode based on preferences and policy impacts"""
        # Base preferences
        preferences = self.transport_preferences.copy()
        
        # Apply policy impacts (e.g., bus lane expansion, EV incentives)
        if 'transit_improvement' in policy_impacts:
            preferences[TransportMode.TRANSIT] *= 1.2
        
        if 'bike_infrastructure' in policy_impacts:
            preferences[TransportMode.BIKE] *= 1.3
        
        if 'ev_incentives' in policy_impacts and self.income_level in ['medium', 'high']:
            preferences[TransportMode.EV] = preferences.get(TransportMode.CAR, 0) * 0.3
            preferences[TransportMode.CAR] *= 0.7
        
        # Normalize preferences
        total = sum(preferences.values())
        if total > 0:
            preferences = {k: v/total for k, v in preferences.items()}
        
        # Choose mode based on probabilities
        modes = list(preferences.keys())
        probabilities = list(preferences.values())
        return np.random.choice(modes, p=probabilities)
    
    def calculate_route(self, destination: Location, transport_mode: TransportMode, 
                       network: nx.Graph) -> Route:
        """Calculate route from current location to destination"""
        # Simplified route calculation
        # In a real implementation, this would use routing algorithms
        
        distance = self._calculate_distance(self.current_location, destination)
        
        # Base travel time by mode
        speed_kmh = {
            TransportMode.CAR: 30,
            TransportMode.TRANSIT: 20,
            TransportMode.BIKE: 15,
            TransportMode.WALK: 5,
            TransportMode.EV: 30
        }
        
        travel_time = (distance / speed_kmh[transport_mode]) * 60  # minutes
        
        return Route(
            origin=self.current_location,
            destination=destination,
            waypoints=[self.current_location, destination],
            distance_km=distance,
            travel_time_minutes=travel_time,
            transport_mode=transport_mode
        )
    
    def _calculate_distance(self, origin: Location, destination: Location) -> float:
        """Calculate distance between two points (simplified)"""
        # Haversine formula would be used in production
        lat_diff = abs(origin.lat - destination.lat)
        lng_diff = abs(origin.lng - destination.lng)
        return np.sqrt(lat_diff**2 + lng_diff**2) * 111  # Rough km conversion
    
    def update_behavior(self, timestep: int, route: Route, policy_impacts: Dict[str, Any]):
        """Update agent behavior for current timestep"""
        # Calculate environmental impact
        co2_emissions = self._calculate_co2_emissions(route)
        energy_consumption = self._calculate_energy_consumption(route)
        
        behavior = {
            'timestep': timestep,
            'location': {'lat': route.destination.lat, 'lng': route.destination.lng},
            'activity': self.current_activity,
            'transport_mode': route.transport_mode.value,
            'origin': {'lat': route.origin.lat, 'lng': route.origin.lng},
            'destination': {'lat': route.destination.lat, 'lng': route.destination.lng},
            'travel_time_minutes': route.travel_time_minutes,
            'distance_km': route.distance_km,
            'route': [{'lat': wp.lat, 'lng': wp.lng} for wp in route.waypoints],
            'co2_emissions_kg': co2_emissions,
            'energy_consumption_kwh': energy_consumption
        }
        
        self.behavior_history.append(behavior)
        self.current_location = route.destination
        self.current_route = route
    
    def _calculate_co2_emissions(self, route: Route) -> float:
        """Calculate CO2 emissions for the route"""
        # Emissions factors (kg CO2 per km)
        emissions_factors = {
            TransportMode.CAR: 0.12,
            TransportMode.TRANSIT: 0.05,
            TransportMode.BIKE: 0.0,
            TransportMode.WALK: 0.0,
            TransportMode.EV: 0.03
        }
        
        return route.distance_km * emissions_factors.get(route.transport_mode, 0.12)
    
    def _calculate_energy_consumption(self, route: Route) -> float:
        """Calculate energy consumption for the route"""
        # Energy consumption factors (kWh per km)
        energy_factors = {
            TransportMode.CAR: 0.6,
            TransportMode.TRANSIT: 0.3,
            TransportMode.BIKE: 0.0,
            TransportMode.WALK: 0.0,
            TransportMode.EV: 0.2
        }
        
        return route.distance_km * energy_factors.get(route.transport_mode, 0.6)


class UrbanNetwork:
    """Urban transportation network"""
    
    def __init__(self, city_data: Dict[str, Any]):
        self.graph = nx.Graph()
        self.road_network = city_data.get('road_network', {})
        self.transit_network = city_data.get('transit_network', {})
        self.bike_network = city_data.get('bike_network', {})
        
        self._build_network()
    
    def _build_network(self):
        """Build the transportation network graph"""
        # Add road network nodes and edges
        for road in self.road_network.get('roads', []):
            self.graph.add_edge(
                road['start_node'], 
                road['end_node'],
                road_type='road',
                capacity=road.get('capacity', 1000),
                speed_limit=road.get('speed_limit', 50)
            )
        
        # Add transit network
        for route in self.transit_network.get('routes', []):
            for i in range(len(route['stops']) - 1):
                self.graph.add_edge(
                    route['stops'][i],
                    route['stops'][i + 1],
                    road_type='transit',
                    capacity=route.get('capacity', 100),
                    frequency=route.get('frequency', 10)
                )
        
        # Add bike network
        for bike_path in self.bike_network.get('paths', []):
            self.graph.add_edge(
                bike_path['start_node'],
                bike_path['end_node'],
                road_type='bike',
                capacity=bike_path.get('capacity', 50)
            )
    
    def get_route(self, origin: Location, destination: Location, 
                  transport_mode: TransportMode) -> List[Location]:
        """Get route between two locations"""
        # Simplified routing - in production would use proper routing algorithms
        return [origin, destination]


class SimulationEngine:
    """Main simulation engine for urban planning"""
    
    def __init__(self):
        self.agents: List[UrbanAgent] = []
        self.network: Optional[UrbanNetwork] = None
        self.policies: List[Policy] = []
        self.current_timestep = 0
        self.results = {}
    
    async def initialize_simulation(self, city: City, policies: List[Policy], 
                                  agent_count: int = 1000) -> None:
        """Initialize the simulation with city data and policies"""
        logger.info(f"Initializing simulation for {city.name} with {agent_count} agents")
        
        # Load city data
        city_data = await self._load_city_data(city)
        
        # Build transportation network
        self.network = UrbanNetwork(city_data)
        
        # Create agents
        await self._create_agents(city, agent_count)
        
        # Store policies
        self.policies = policies
        
        logger.info(f"Simulation initialized with {len(self.agents)} agents")
    
    async def _load_city_data(self, city: City) -> Dict[str, Any]:
        """Load city data for simulation"""
        # In production, this would load from database
        return {
            'road_network': {
                'roads': [
                    {
                        'start_node': 'node1',
                        'end_node': 'node2',
                        'capacity': 1000,
                        'speed_limit': 50
                    }
                ]
            },
            'transit_network': {
                'routes': [
                    {
                        'stops': ['stop1', 'stop2', 'stop3'],
                        'capacity': 100,
                        'frequency': 10
                    }
                ]
            },
            'bike_network': {
                'paths': [
                    {
                        'start_node': 'bike1',
                        'end_node': 'bike2',
                        'capacity': 50
                    }
                ]
            }
        }
    
    async def _create_agents(self, city: City, agent_count: int) -> None:
        """Create agents for the simulation"""
        self.agents = []
        
        for i in range(agent_count):
            # Generate random agent properties
            agent_type = np.random.choice(list(AgentType))
            
            properties = {
                'home_location': Location(
                    lat=city.latitude + np.random.normal(0, 0.01),
                    lng=city.longitude + np.random.normal(0, 0.01)
                ),
                'work_location': Location(
                    lat=city.latitude + np.random.normal(0, 0.01),
                    lng=city.longitude + np.random.normal(0, 0.01)
                ),
                'income_level': np.random.choice(['low', 'medium', 'high'], p=[0.3, 0.5, 0.2]),
                'age_group': np.random.choice(['young', 'adult', 'senior'], p=[0.2, 0.6, 0.2]),
                'household_size': np.random.poisson(2.5),
                'vehicle_type': np.random.choice(['gas', 'hybrid', 'electric'], p=[0.7, 0.2, 0.1])
            }
            
            agent = UrbanAgent(f"agent_{i}", agent_type, properties)
            self.agents.append(agent)
    
    async def run_simulation(self, timesteps: int = 1000) -> Dict[str, Any]:
        """Run the simulation for specified number of timesteps"""
        logger.info(f"Starting simulation for {timesteps} timesteps")
        
        self.current_timestep = 0
        self.results = {
            'total_co2_emissions': 0,
            'total_energy_consumption': 0,
            'total_travel_time': 0,
            'modal_split': {},
            'agent_behaviors': []
        }
        
        for timestep in range(timesteps):
            await self._simulate_timestep(timestep)
            self.current_timestep = timestep
            
            # Progress logging
            if timestep % 100 == 0:
                logger.info(f"Simulation progress: {timestep}/{timesteps}")
        
        # Calculate final results
        self._calculate_final_results()
        
        logger.info("Simulation completed")
        return self.results
    
    async def _simulate_timestep(self, timestep: int) -> None:
        """Simulate a single timestep"""
        policy_impacts = self._calculate_policy_impacts()
        
        for agent in self.agents:
            # Determine agent's destination for this timestep
            destination = self._determine_destination(agent, timestep)
            
            if destination and destination != agent.current_location:
                # Calculate route
                transport_mode = agent.choose_transport_mode(
                    Route(agent.current_location, destination, [], 0, 0, TransportMode.CAR),
                    policy_impacts
                )
                
                route = agent.calculate_route(destination, transport_mode, self.network.graph)
                
                # Update agent behavior
                agent.update_behavior(timestep, route, policy_impacts)
                
                # Update simulation results
                self._update_results(agent.behavior_history[-1])
    
    def _calculate_policy_impacts(self) -> Dict[str, Any]:
        """Calculate impacts of active policies"""
        impacts = {}
        
        for policy in self.policies:
            if policy.status == 'active':
                for component in policy.policy_components:
                    if component.component_type == 'bus_lane':
                        impacts['transit_improvement'] = True
                    elif component.component_type == 'bike_lane':
                        impacts['bike_infrastructure'] = True
                    elif component.component_type == 'ev_charging':
                        impacts['ev_incentives'] = True
        
        return impacts
    
    def _determine_destination(self, agent: UrbanAgent, timestep: int) -> Optional[Location]:
        """Determine agent's destination for current timestep"""
        # Simplified destination logic
        # In production, this would use activity-based modeling
        
        hour = (timestep % 24)  # Assume each timestep is 1 hour
        
        if 6 <= hour <= 9:  # Morning commute
            return agent.work_location
        elif 17 <= hour <= 19:  # Evening commute
            return agent.home_location
        elif 10 <= hour <= 16:  # Work hours
            return agent.work_location
        else:  # Evening/night
            return agent.home_location
    
    def _update_results(self, behavior: Dict[str, Any]) -> None:
        """Update simulation results with agent behavior"""
        self.results['total_co2_emissions'] += behavior['co2_emissions_kg']
        self.results['total_energy_consumption'] += behavior['energy_consumption_kwh']
        self.results['total_travel_time'] += behavior['travel_time_minutes']
        
        # Update modal split
        mode = behavior['transport_mode']
        self.results['modal_split'][mode] = self.results['modal_split'].get(mode, 0) + 1
        
        # Store behavior data
        self.results['agent_behaviors'].append(behavior)
    
    def _calculate_final_results(self) -> None:
        """Calculate final simulation results"""
        # Normalize modal split to percentages
        total_trips = sum(self.results['modal_split'].values())
        if total_trips > 0:
            self.results['modal_split'] = {
                mode: (count / total_trips) * 100 
                for mode, count in self.results['modal_split'].items()
            }
        
        # Calculate averages
        if len(self.results['agent_behaviors']) > 0:
            self.results['avg_travel_time'] = (
                self.results['total_travel_time'] / len(self.results['agent_behaviors'])
            )
            self.results['avg_co2_per_trip'] = (
                self.results['total_co2_emissions'] / len(self.results['agent_behaviors'])
            )
    
    async def save_simulation_results(self, simulation_run: SimulationRun) -> None:
        """Save simulation results to database"""
        # This would save to database in production
        logger.info(f"Saving simulation results for run {simulation_run.id}")
        
        # Update simulation run with results
        simulation_run.results = self.results
        simulation_run.metrics = {
            'total_agents': len(self.agents),
            'total_timesteps': self.current_timestep + 1,
            'total_co2_emissions': self.results['total_co2_emissions'],
            'total_energy_consumption': self.results['total_energy_consumption'],
            'avg_travel_time': self.results.get('avg_travel_time', 0),
            'modal_split': self.results['modal_split']
        }
        
        # Save agent behaviors
        for behavior in self.results['agent_behaviors']:
            # Create AgentBehavior record
            pass  # Would save to database
