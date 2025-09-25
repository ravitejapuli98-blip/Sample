"""
Policy recommendation and optimization engine
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass
from enum import Enum

from app.models.policy import Policy, PolicyComponent, PolicyPackage, PolicyRecommendation
from app.models.city import City, MobilityData, AirQualityData, EnergyData, Neighborhood
from app.models.simulation import Simulation, SimulationRun
from app.models.prediction import PredictionModel, Prediction

logger = logging.getLogger(__name__)


class PolicyCategory(Enum):
    TRANSPORTATION = "transportation"
    ENERGY = "energy"
    AIR_QUALITY = "air_quality"
    LAND_USE = "land_use"
    SOCIAL_EQUITY = "social_equity"


class PolicyType(Enum):
    INFRASTRUCTURE = "infrastructure"
    REGULATION = "regulation"
    INCENTIVE = "incentive"
    EDUCATION = "education"
    TECHNOLOGY = "technology"


@dataclass
class PolicyImpact:
    """Expected impact of a policy"""
    co2_reduction_tonnes: float
    pm25_reduction_ug_m3: float
    travel_time_reduction_minutes: float
    energy_savings_mwh: float
    cost_benefit_ratio: float
    equity_score: float
    implementation_cost: float
    timeline_months: int


@dataclass
class PolicyConstraint:
    """Constraints for policy optimization"""
    max_budget: float
    max_timeline_months: int
    min_equity_score: float
    required_co2_reduction: float
    excluded_policy_types: List[PolicyType]


class PolicyRecommendationEngine:
    """AI-powered policy recommendation engine"""
    
    def __init__(self):
        self.policy_templates = self._load_policy_templates()
        self.impact_models = {}
        self.equity_weights = {
            'low_income_benefit': 0.3,
            'accessibility_improvement': 0.25,
            'environmental_justice': 0.25,
            'health_benefits': 0.2
        }
    
    def _load_policy_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined policy templates"""
        return {
            'bus_lane_expansion': {
                'name': 'Bus Lane Expansion',
                'category': PolicyCategory.TRANSPORTATION,
                'type': PolicyType.INFRASTRUCTURE,
                'description': 'Expand dedicated bus lanes to improve public transit efficiency',
                'base_cost_per_km': 500000,
                'base_timeline_months': 12,
                'impact_factors': {
                    'transit_ridership_increase': 0.15,
                    'travel_time_reduction': 0.1,
                    'co2_reduction_per_km': 0.05,
                    'equity_benefit': 0.8
                }
            },
            'ev_charging_network': {
                'name': 'EV Charging Network',
                'category': PolicyCategory.ENERGY,
                'type': PolicyType.INFRASTRUCTURE,
                'description': 'Deploy public EV charging stations across the city',
                'base_cost_per_station': 50000,
                'base_timeline_months': 18,
                'impact_factors': {
                    'ev_adoption_increase': 0.2,
                    'co2_reduction_per_station': 0.1,
                    'energy_demand_increase': 0.05,
                    'equity_benefit': 0.6
                }
            },
            'bike_lane_network': {
                'name': 'Protected Bike Lane Network',
                'category': PolicyCategory.TRANSPORTATION,
                'type': PolicyType.INFRASTRUCTURE,
                'description': 'Build protected bike lanes to encourage cycling',
                'base_cost_per_km': 200000,
                'base_timeline_months': 8,
                'impact_factors': {
                    'bike_usage_increase': 0.3,
                    'traffic_reduction': 0.05,
                    'co2_reduction_per_km': 0.08,
                    'equity_benefit': 0.7
                }
            },
            'congestion_pricing': {
                'name': 'Congestion Pricing',
                'category': PolicyCategory.TRANSPORTATION,
                'type': PolicyType.REGULATION,
                'description': 'Implement congestion pricing in city center',
                'base_cost': 2000000,
                'base_timeline_months': 24,
                'impact_factors': {
                    'traffic_reduction': 0.2,
                    'transit_ridership_increase': 0.1,
                    'co2_reduction': 0.15,
                    'revenue_generation': 0.3,
                    'equity_benefit': 0.4
                }
            },
            'solar_rooftop_program': {
                'name': 'Solar Rooftop Incentive Program',
                'category': PolicyCategory.ENERGY,
                'type': PolicyType.INCENTIVE,
                'description': 'Subsidize residential and commercial solar installations',
                'base_cost_per_kw': 3000,
                'base_timeline_months': 36,
                'impact_factors': {
                    'solar_adoption_increase': 0.4,
                    'co2_reduction_per_kw': 0.12,
                    'energy_independence': 0.2,
                    'equity_benefit': 0.5
                }
            },
            'green_building_standards': {
                'name': 'Green Building Standards',
                'category': PolicyCategory.ENERGY,
                'type': PolicyType.REGULATION,
                'description': 'Mandate energy efficiency standards for new buildings',
                'base_cost': 500000,
                'base_timeline_months': 6,
                'impact_factors': {
                    'energy_efficiency_improvement': 0.25,
                    'co2_reduction_per_building': 0.1,
                    'construction_cost_increase': 0.05,
                    'equity_benefit': 0.3
                }
            }
        }
    
    async def recommend_policies(self, city: City, constraints: PolicyConstraint,
                               current_data: Dict[str, Any]) -> List[PolicyRecommendation]:
        """Generate policy recommendations for a city"""
        logger.info(f"Generating policy recommendations for {city.name}")
        
        recommendations = []
        
        # Analyze current city conditions
        city_analysis = await self._analyze_city_conditions(city, current_data)
        
        # Score each policy template
        policy_scores = {}
        for template_id, template in self.policy_templates.items():
            score = await self._score_policy_template(
                template, city_analysis, constraints
            )
            policy_scores[template_id] = score
        
        # Sort policies by score
        sorted_policies = sorted(
            policy_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Generate recommendations
        for template_id, score in sorted_policies[:5]:  # Top 5 policies
            template = self.policy_templates[template_id]
            
            # Calculate policy parameters
            policy_params = await self._calculate_policy_parameters(
                template, city_analysis, constraints
            )
            
            # Estimate impacts
            impacts = await self._estimate_policy_impacts(
                template, policy_params, city_analysis
            )
            
            # Create recommendation
            recommendation = PolicyRecommendation(
                city_id=city.id,
                title=template['name'],
                description=template['description'],
                rationale=self._generate_rationale(template, city_analysis, impacts),
                recommendation_type=self._determine_recommendation_type(impacts),
                priority_score=score,
                expected_outcomes=impacts.__dict__,
                confidence_score=self._calculate_confidence_score(template, city_analysis),
                estimated_cost=impacts.implementation_cost,
                implementation_difficulty=self._assess_implementation_difficulty(template),
                timeline_months=impacts.timeline_months,
                status='generated'
            )
            
            recommendations.append(recommendation)
        
        logger.info(f"Generated {len(recommendations)} policy recommendations")
        return recommendations
    
    async def _analyze_city_conditions(self, city: City, 
                                     current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current city conditions to inform policy recommendations"""
        analysis = {
            'population': city.population,
            'area_km2': city.area_km2,
            'density': city.population / city.area_km2 if city.area_km2 else 0,
            'mobility_issues': [],
            'energy_issues': [],
            'air_quality_issues': [],
            'equity_issues': []
        }
        
        # Analyze mobility data
        if 'mobility_data' in current_data:
            mobility = current_data['mobility_data']
            if mobility.get('congestion_level', 0) > 0.7:
                analysis['mobility_issues'].append('high_congestion')
            if mobility.get('public_transit_share', 0) < 0.2:
                analysis['mobility_issues'].append('low_transit_usage')
            if mobility.get('bike_share', 0) < 0.05:
                analysis['mobility_issues'].append('low_bike_usage')
        
        # Analyze energy data
        if 'energy_data' in current_data:
            energy = current_data['energy_data']
            if energy.get('renewable_percentage', 0) < 0.2:
                analysis['energy_issues'].append('low_renewable_share')
            if energy.get('grid_efficiency', 1.0) < 0.8:
                analysis['energy_issues'].append('low_grid_efficiency')
        
        # Analyze air quality data
        if 'air_quality_data' in current_data:
            air_quality = current_data['air_quality_data']
            if air_quality.get('pm25_ug_m3', 0) > 15:
                analysis['air_quality_issues'].append('high_pm25')
            if air_quality.get('aqi', 0) > 100:
                analysis['air_quality_issues'].append('poor_air_quality')
        
        return analysis
    
    async def _score_policy_template(self, template: Dict[str, Any], 
                                   city_analysis: Dict[str, Any],
                                   constraints: PolicyConstraint) -> float:
        """Score a policy template based on city conditions and constraints"""
        score = 0.0
        
        # Base score from template
        base_score = 0.5
        
        # Adjust based on city issues
        category = template['category']
        if category == PolicyCategory.TRANSPORTATION:
            if 'high_congestion' in city_analysis['mobility_issues']:
                score += 0.3
            if 'low_transit_usage' in city_analysis['mobility_issues']:
                score += 0.2
        elif category == PolicyCategory.ENERGY:
            if 'low_renewable_share' in city_analysis['energy_issues']:
                score += 0.3
        elif category == PolicyCategory.AIR_QUALITY:
            if 'high_pm25' in city_analysis['air_quality_issues']:
                score += 0.3
        
        # Adjust based on constraints
        if template['type'] in constraints.excluded_policy_types:
            score = 0.0
        
        # Adjust based on budget
        estimated_cost = template.get('base_cost', 1000000)
        if estimated_cost > constraints.max_budget:
            score *= 0.5
        
        # Adjust based on timeline
        estimated_timeline = template.get('base_timeline_months', 12)
        if estimated_timeline > constraints.max_timeline_months:
            score *= 0.7
        
        return min(score + base_score, 1.0)
    
    async def _calculate_policy_parameters(self, template: Dict[str, Any],
                                         city_analysis: Dict[str, Any],
                                         constraints: PolicyConstraint) -> Dict[str, Any]:
        """Calculate specific parameters for a policy based on city conditions"""
        params = template.copy()
        
        # Scale based on city size
        if 'base_cost_per_km' in params:
            # Estimate network size based on city area
            network_km = np.sqrt(city_analysis['area_km2']) * 2
            params['total_cost'] = params['base_cost_per_km'] * network_km
        elif 'base_cost_per_station' in params:
            # Estimate number of stations based on population
            stations = max(10, city_analysis['population'] // 10000)
            params['total_cost'] = params['base_cost_per_station'] * stations
        elif 'base_cost_per_kw' in params:
            # Estimate solar capacity based on population
            capacity_kw = city_analysis['population'] * 0.5  # 0.5 kW per person
            params['total_cost'] = params['base_cost_per_kw'] * capacity_kw
        
        # Apply budget constraints
        if params.get('total_cost', 0) > constraints.max_budget:
            scale_factor = constraints.max_budget / params['total_cost']
            params['total_cost'] = constraints.max_budget
            params['scale_factor'] = scale_factor
        
        return params
    
    async def _estimate_policy_impacts(self, template: Dict[str, Any],
                                     params: Dict[str, Any],
                                     city_analysis: Dict[str, Any]) -> PolicyImpact:
        """Estimate the impacts of implementing a policy"""
        impact_factors = template.get('impact_factors', {})
        
        # Calculate CO2 reduction
        co2_reduction = 0.0
        if 'co2_reduction_per_km' in impact_factors:
            network_km = np.sqrt(city_analysis['area_km2']) * 2
            co2_reduction = impact_factors['co2_reduction_per_km'] * network_km * 1000  # tonnes
        elif 'co2_reduction_per_station' in impact_factors:
            stations = max(10, city_analysis['population'] // 10000)
            co2_reduction = impact_factors['co2_reduction_per_station'] * stations * 1000
        elif 'co2_reduction' in impact_factors:
            co2_reduction = impact_factors['co2_reduction'] * 1000  # tonnes
        
        # Calculate PM2.5 reduction
        pm25_reduction = co2_reduction * 0.1  # Rough correlation
        
        # Calculate travel time reduction
        travel_time_reduction = 0.0
        if 'travel_time_reduction' in impact_factors:
            travel_time_reduction = impact_factors['travel_time_reduction'] * 30  # minutes
        
        # Calculate energy savings
        energy_savings = 0.0
        if 'energy_efficiency_improvement' in impact_factors:
            energy_savings = impact_factors['energy_efficiency_improvement'] * 1000  # MWh
        
        # Calculate cost-benefit ratio
        cost_benefit_ratio = 1.0
        if 'revenue_generation' in impact_factors:
            annual_revenue = impact_factors['revenue_generation'] * params.get('total_cost', 1000000)
            cost_benefit_ratio = annual_revenue / params.get('total_cost', 1000000)
        
        # Calculate equity score
        equity_score = impact_factors.get('equity_benefit', 0.5)
        
        return PolicyImpact(
            co2_reduction_tonnes=co2_reduction,
            pm25_reduction_ug_m3=pm25_reduction,
            travel_time_reduction_minutes=travel_time_reduction,
            energy_savings_mwh=energy_savings,
            cost_benefit_ratio=cost_benefit_ratio,
            equity_score=equity_score,
            implementation_cost=params.get('total_cost', 1000000),
            timeline_months=params.get('base_timeline_months', 12)
        )
    
    def _generate_rationale(self, template: Dict[str, Any], 
                          city_analysis: Dict[str, Any],
                          impacts: PolicyImpact) -> str:
        """Generate rationale for policy recommendation"""
        rationale_parts = []
        
        # Address specific city issues
        category = template['category']
        if category == PolicyCategory.TRANSPORTATION:
            if 'high_congestion' in city_analysis['mobility_issues']:
                rationale_parts.append("Addresses high traffic congestion")
            if 'low_transit_usage' in city_analysis['mobility_issues']:
                rationale_parts.append("Improves public transit accessibility")
        
        # Highlight key benefits
        if impacts.co2_reduction_tonnes > 1000:
            rationale_parts.append(f"Significant CO2 reduction of {impacts.co2_reduction_tonnes:.0f} tonnes annually")
        
        if impacts.equity_score > 0.7:
            rationale_parts.append("High equity benefits for underserved communities")
        
        if impacts.cost_benefit_ratio > 1.5:
            rationale_parts.append("Strong cost-benefit ratio with potential revenue generation")
        
        return ". ".join(rationale_parts) + "."
    
    def _determine_recommendation_type(self, impacts: PolicyImpact) -> str:
        """Determine the type of recommendation based on impacts"""
        if impacts.timeline_months <= 6 and impacts.implementation_cost < 500000:
            return "quick_win"
        elif impacts.co2_reduction_tonnes > 5000:
            return "high_impact"
        elif impacts.equity_score > 0.8:
            return "equity_focused"
        else:
            return "long_term"
    
    def _calculate_confidence_score(self, template: Dict[str, Any],
                                  city_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the recommendation"""
        confidence = 0.7  # Base confidence
        
        # Increase confidence for well-studied policies
        if template['type'] == PolicyType.INFRASTRUCTURE:
            confidence += 0.1
        
        # Increase confidence if city has similar characteristics to case studies
        if city_analysis['density'] > 1000:  # High density city
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _assess_implementation_difficulty(self, template: Dict[str, Any]) -> str:
        """Assess implementation difficulty of a policy"""
        timeline = template.get('base_timeline_months', 12)
        cost = template.get('base_cost', 1000000)
        
        if timeline <= 6 and cost <= 500000:
            return "low"
        elif timeline <= 18 and cost <= 2000000:
            return "medium"
        else:
            return "high"


class PolicyOptimizationEngine:
    """Engine for optimizing policy packages"""
    
    def __init__(self):
        self.recommendation_engine = PolicyRecommendationEngine()
    
    async def optimize_policy_package(self, city: City, constraints: PolicyConstraint,
                                    current_data: Dict[str, Any]) -> PolicyPackage:
        """Optimize a package of policies to maximize impact within constraints"""
        logger.info(f"Optimizing policy package for {city.name}")
        
        # Get individual policy recommendations
        recommendations = await self.recommendation_engine.recommend_policies(
            city, constraints, current_data
        )
        
        # Use optimization algorithm to select best combination
        optimal_policies = await self._optimize_policy_combination(
            recommendations, constraints
        )
        
        # Create policy package
        package = PolicyPackage(
            name=f"Optimized Policy Package for {city.name}",
            description="AI-optimized combination of policies for maximum impact",
            total_cost=sum(p.estimated_cost for p in optimal_policies),
            implementation_timeline_months=max(p.timeline_months for p in optimal_policies),
            expected_benefits=self._calculate_package_benefits(optimal_policies),
            status='draft'
        )
        
        logger.info(f"Created optimized policy package with {len(optimal_policies)} policies")
        return package
    
    async def _optimize_policy_combination(self, recommendations: List[PolicyRecommendation],
                                         constraints: PolicyConstraint) -> List[PolicyRecommendation]:
        """Use optimization algorithm to select best policy combination"""
        # Simplified greedy optimization
        # In production, would use more sophisticated algorithms (genetic algorithm, etc.)
        
        selected_policies = []
        remaining_budget = constraints.max_budget
        remaining_timeline = constraints.max_timeline_months
        
        # Sort by priority score
        sorted_recommendations = sorted(
            recommendations, 
            key=lambda x: x.priority_score, 
            reverse=True
        )
        
        for recommendation in sorted_recommendations:
            if (recommendation.estimated_cost <= remaining_budget and
                recommendation.timeline_months <= remaining_timeline and
                self._check_policy_compatibility(recommendation, selected_policies)):
                
                selected_policies.append(recommendation)
                remaining_budget -= recommendation.estimated_cost
                remaining_timeline = min(remaining_timeline, recommendation.timeline_months)
        
        return selected_policies
    
    def _check_policy_compatibility(self, new_policy: PolicyRecommendation,
                                  existing_policies: List[PolicyRecommendation]) -> bool:
        """Check if a policy is compatible with existing policies"""
        # Simple compatibility check
        # In production, would have more sophisticated compatibility rules
        
        for existing in existing_policies:
            # Avoid duplicate policies
            if new_policy.title == existing.title:
                return False
            
            # Check for conflicting policies
            if (new_policy.title == "Congestion Pricing" and 
                existing.title == "Bus Lane Expansion"):
                return False  # These might conflict
        
        return True
    
    def _calculate_package_benefits(self, policies: List[PolicyRecommendation]) -> Dict[str, Any]:
        """Calculate combined benefits of a policy package"""
        total_co2_reduction = sum(
            p.expected_outcomes.get('co2_reduction_tonnes', 0) 
            for p in policies
        )
        
        total_cost = sum(p.estimated_cost for p in policies)
        
        avg_equity_score = np.mean([
            p.expected_outcomes.get('equity_score', 0.5) 
            for p in policies
        ])
        
        return {
            'total_co2_reduction_tonnes': total_co2_reduction,
            'total_cost': total_cost,
            'average_equity_score': avg_equity_score,
            'policy_count': len(policies),
            'estimated_roi': total_co2_reduction * 100 / total_cost if total_cost > 0 else 0
        }
