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
        "version": "1.0.0"
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
                "sustainability_score": 78
            },
            {
                "id": 2,
                "name": "Portland",
                "population": 652503,
                "area_km2": 376.5,
                "emissions_tonnes_co2": 1800000,
                "air_quality_index": 35,
                "sustainability_score": 85
            },
            {
                "id": 3,
                "name": "Seattle",
                "population": 749256,
                "area_km2": 369.2,
                "emissions_tonnes_co2": 2200000,
                "air_quality_index": 42,
                "sustainability_score": 82
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
                "priority": "high"
            },
            {
                "id": 2,
                "name": "EV Charging Infrastructure",
                "type": "energy",
                "description": "Install 1000 new EV charging stations across the city",
                "estimated_cost": 25000000,
                "co2_reduction_percent": 8,
                "implementation_time_months": 12,
                "priority": "medium"
            },
            {
                "id": 3,
                "name": "Green Building Standards",
                "type": "construction",
                "description": "Mandate LEED certification for all new commercial buildings",
                "estimated_cost": 15000000,
                "co2_reduction_percent": 12,
                "implementation_time_months": 24,
                "priority": "high"
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
                "results": {
                    "travel_time_reduction": 12,
                    "emissions_reduction": 18,
                    "cost_benefit_ratio": 2.3,
                    "equity_impact": "positive"
                },
                "created_at": "2024-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "name": "Energy Grid Analysis",
                "status": "running",
                "city_id": 2,
                "results": {
                    "estimated_completion": "2024-01-20T15:00:00Z"
                },
                "created_at": "2024-01-18T09:15:00Z"
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
                "time_horizon_years": 5
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
