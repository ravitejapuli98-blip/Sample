from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="AI Sustainable Cities Planner",
    description="Multi-agent simulation and planning tool for sustainable urban development",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI Sustainable Cities Planner API", 
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "cities": "/api/v1/cities",
            "policies": "/api/v1/policies",
            "simulations": "/api/v1/simulations",
            "predictions": "/api/v1/predictions",
            "ai": "/api/v1/ai",
            "real-data": "/api/v1/real-data"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sustainable-cities-planner"}

@app.get("/api/v1/cities")
async def get_cities():
    return {
        "cities": [
            {
                "id": 1,
                "name": "San Francisco",
                "population": 873965,
                "area_km2": 121.4,
                "emissions_tonnes_co2": 2500000,
                "air_quality_index": 45,
                "sustainability_score": 78,
                "transportation_mode_share": {
                    "public_transit": 35,
                    "walking": 15,
                    "cycling": 8,
                    "driving": 42
                }
            },
            {
                "id": 2,
                "name": "Portland",
                "population": 652503,
                "area_km2": 376.5,
                "emissions_tonnes_co2": 1800000,
                "air_quality_index": 35,
                "sustainability_score": 85,
                "transportation_mode_share": {
                    "public_transit": 25,
                    "walking": 20,
                    "cycling": 12,
                    "driving": 43
                }
            },
            {
                "id": 3,
                "name": "Seattle",
                "population": 749256,
                "area_km2": 369.2,
                "emissions_tonnes_co2": 2200000,
                "air_quality_index": 42,
                "sustainability_score": 82,
                "transportation_mode_share": {
                    "public_transit": 30,
                    "walking": 18,
                    "cycling": 10,
                    "driving": 42
                }
            }
        ]
    }

@app.get("/api/v1/policies")
async def get_policies():
    return {
        "policies": [
            {
                "id": 1,
                "name": "Bus Lane Expansion",
                "type": "transportation",
                "description": "Expand dedicated bus lanes to improve public transit efficiency",
                "estimated_cost": 50000000,
                "co2_reduction_percent": 15,
                "implementation_time_months": 18,
                "priority": "high",
                "target_cities": [1, 2, 3],
                "expected_benefits": {
                    "travel_time_reduction": 12,
                    "ridership_increase": 25,
                    "emissions_reduction": 15
                }
            },
            {
                "id": 2,
                "name": "EV Charging Infrastructure",
                "type": "energy",
                "description": "Install 1000 new EV charging stations across the city",
                "estimated_cost": 25000000,
                "co2_reduction_percent": 8,
                "implementation_time_months": 12,
                "priority": "medium",
                "target_cities": [1, 2, 3],
                "expected_benefits": {
                    "ev_adoption_increase": 40,
                    "emissions_reduction": 8,
                    "air_quality_improvement": 5
                }
            },
            {
                "id": 3,
                "name": "Green Building Standards",
                "type": "construction",
                "description": "Mandate LEED certification for all new commercial buildings",
                "estimated_cost": 15000000,
                "co2_reduction_percent": 12,
                "implementation_time_months": 24,
                "priority": "high",
                "target_cities": [1, 2, 3],
                "expected_benefits": {
                    "energy_efficiency": 20,
                    "emissions_reduction": 12,
                    "water_usage_reduction": 15
                }
            },
            {
                "id": 4,
                "name": "Smart Traffic Management",
                "type": "technology",
                "description": "Implement AI-powered traffic signal optimization",
                "estimated_cost": 30000000,
                "co2_reduction_percent": 10,
                "implementation_time_months": 15,
                "priority": "medium",
                "target_cities": [1, 2, 3],
                "expected_benefits": {
                    "traffic_flow_improvement": 18,
                    "emissions_reduction": 10,
                    "fuel_savings": 12
                }
            }
        ]
    }

@app.get("/api/v1/simulations")
async def get_simulations():
    return {
        "simulations": [
            {
                "id": 1,
                "name": "Transportation Optimization",
                "status": "completed",
                "city_id": 1,
                "policy_ids": [1, 4],
                "results": {
                    "travel_time_reduction": 12,
                    "emissions_reduction": 18,
                    "cost_benefit_ratio": 2.3,
                    "equity_impact": "positive",
                    "implementation_feasibility": 0.85
                },
                "created_at": "2024-01-15T10:30:00Z",
                "completed_at": "2024-01-15T14:45:00Z"
            },
            {
                "id": 2,
                "name": "Energy Grid Analysis",
                "status": "running",
                "city_id": 2,
                "policy_ids": [2, 3],
                "results": {
                    "estimated_completion": "2024-01-20T15:00:00Z",
                    "progress_percentage": 65
                },
                "created_at": "2024-01-18T09:15:00Z"
            },
            {
                "id": 3,
                "name": "Comprehensive City Transformation",
                "status": "completed",
                "city_id": 3,
                "policy_ids": [1, 2, 3, 4],
                "results": {
                    "overall_emissions_reduction": 25,
                    "sustainability_score_improvement": 15,
                    "cost_benefit_ratio": 1.8,
                    "equity_impact": "positive",
                    "implementation_feasibility": 0.72
                },
                "created_at": "2024-01-10T08:00:00Z",
                "completed_at": "2024-01-12T16:30:00Z"
            }
        ]
    }

@app.get("/api/v1/predictions")
async def get_predictions():
    return {
        "predictions": [
            {
                "id": 1,
                "policy_id": 1,
                "city_id": 1,
                "predicted_emissions_reduction": 18.5,
                "predicted_cost_savings": 12000000,
                "confidence_score": 0.87,
                "time_horizon_years": 5,
                "risk_factors": ["construction_delays", "public_opposition"],
                "success_probability": 0.82
            },
            {
                "id": 2,
                "policy_id": 2,
                "city_id": 2,
                "predicted_emissions_reduction": 8.2,
                "predicted_cost_savings": 8000000,
                "confidence_score": 0.91,
                "time_horizon_years": 3,
                "risk_factors": ["infrastructure_costs"],
                "success_probability": 0.89
            },
            {
                "id": 3,
                "policy_id": 3,
                "city_id": 3,
                "predicted_emissions_reduction": 12.1,
                "predicted_cost_savings": 15000000,
                "confidence_score": 0.79,
                "time_horizon_years": 7,
                "risk_factors": ["regulatory_changes", "market_adoption"],
                "success_probability": 0.75
            }
        ]
    }

@app.get("/api/v1/analytics")
async def get_analytics():
    return {
        "analytics": {
            "total_cities": 3,
            "total_policies": 4,
            "total_simulations": 3,
            "average_sustainability_score": 81.7,
            "total_emissions_reduction_potential": 35.8,
            "total_estimated_cost": 120000000,
            "total_predicted_savings": 35000000,
            "roi": 0.29,
            "most_effective_policy": "Bus Lane Expansion",
            "most_sustainable_city": "Portland"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)