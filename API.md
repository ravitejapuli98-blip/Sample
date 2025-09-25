# AI Sustainable Cities Planner - API Documentation

This document describes the REST API endpoints for the AI Sustainable Cities Planner.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not require authentication. In production, implement JWT or API key authentication.

## Response Format

All API responses follow this format:

```json
{
  "data": {...},
  "message": "Success message",
  "status": "success"
}
```

Error responses:

```json
{
  "error": "Error message",
  "status": "error",
  "status_code": 400
}
```

## Cities API

### Get Cities

```http
GET /cities
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100, max: 1000)
- `search` (string): Search by city name

**Response:**
```json
[
  {
    "id": 1,
    "name": "San Francisco",
    "state": "CA",
    "country": "USA",
    "population": 873965,
    "area_km2": 121.4,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "timezone": "America/Los_Angeles",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Get City by ID

```http
GET /cities/{city_id}
```

### Create City

```http
POST /cities
```

**Request Body:**
```json
{
  "name": "New York",
  "state": "NY",
  "country": "USA",
  "population": 8336817,
  "area_km2": 789.0,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timezone": "America/New_York"
}
```

### Update City

```http
PUT /cities/{city_id}
```

### Delete City

```http
DELETE /cities/{city_id}
```

### Get City Dashboard

```http
GET /cities/{city_id}/dashboard
```

**Response:**
```json
{
  "city": {...},
  "latest_mobility": {...},
  "latest_air_quality": {...},
  "latest_energy": {...},
  "neighborhoods": [...],
  "summary": {
    "total_neighborhoods": 5,
    "avg_travel_time": 25.5,
    "air_quality_index": 45,
    "renewable_percentage": 35.2
  }
}
```

## Mobility Data API

### Get Mobility Data

```http
GET /cities/{city_id}/mobility
```

**Query Parameters:**
- `start_date` (datetime): Start date filter
- `end_date` (datetime): End date filter
- `limit` (int): Number of records to return

### Create Mobility Data

```http
POST /cities/{city_id}/mobility
```

**Request Body:**
```json
{
  "avg_travel_time_minutes": 25.5,
  "congestion_level": 0.7,
  "vehicle_count": 50000,
  "public_transit_ridership": 150000,
  "road_length_km": 1200.5,
  "bike_lane_length_km": 150.2,
  "bus_stops_count": 2500,
  "ev_charging_stations": 500,
  "car_share": 60.0,
  "public_transit_share": 25.0,
  "bike_share": 10.0,
  "walk_share": 5.0
}
```

## Air Quality Data API

### Get Air Quality Data

```http
GET /cities/{city_id}/air-quality
```

### Create Air Quality Data

```http
POST /cities/{city_id}/air-quality
```

**Request Body:**
```json
{
  "pm25_ug_m3": 12.5,
  "pm10_ug_m3": 25.0,
  "no2_ppb": 30.0,
  "o3_ppb": 45.0,
  "co_ppm": 2.5,
  "so2_ppb": 8.0,
  "aqi": 45,
  "aqi_category": "Good",
  "temperature_c": 22.5,
  "humidity_percent": 65.0,
  "wind_speed_mps": 3.2,
  "wind_direction_deg": 180.0,
  "station_latitude": 37.7749,
  "station_longitude": -122.4194,
  "station_name": "Downtown Station"
}
```

## Energy Data API

### Get Energy Data

```http
GET /cities/{city_id}/energy
```

### Create Energy Data

```http
POST /cities/{city_id}/energy
```

**Request Body:**
```json
{
  "total_consumption_mwh": 5000.0,
  "residential_consumption_mwh": 2000.0,
  "commercial_consumption_mwh": 1500.0,
  "industrial_consumption_mwh": 1000.0,
  "transportation_consumption_mwh": 500.0,
  "solar_generation_mwh": 800.0,
  "wind_generation_mwh": 600.0,
  "hydro_generation_mwh": 400.0,
  "renewable_percentage": 36.0,
  "peak_demand_mw": 250.0,
  "grid_efficiency": 0.92,
  "power_outages_count": 2,
  "avg_outage_duration_minutes": 15.5,
  "ev_charging_demand_mw": 25.0,
  "ev_penetration_rate": 5.0,
  "co2_emissions_kg_mwh": 0.4,
  "total_co2_emissions_tonnes": 2000.0
}
```

## Policies API

### Get Policies

```http
GET /policies
```

**Query Parameters:**
- `city_id` (int): Filter by city
- `category` (string): Filter by category
- `status` (string): Filter by status

### Create Policy

```http
POST /policies
```

**Request Body:**
```json
{
  "city_id": 1,
  "name": "Bus Lane Expansion",
  "description": "Expand dedicated bus lanes to improve public transit efficiency",
  "category": "transportation",
  "policy_type": "infrastructure",
  "parameters": {
    "lanes_km": 50,
    "priority_routes": ["Route 1", "Route 2"]
  },
  "implementation_cost": 5000000,
  "implementation_timeline_months": 12,
  "maintenance_cost_annual": 100000,
  "priority": 3
}
```

### Generate Policy Recommendations

```http
POST /policies/recommendations/{city_id}
```

**Request Body:**
```json
{
  "max_budget": 10000000,
  "max_timeline_months": 24,
  "min_equity_score": 0.5,
  "required_co2_reduction": 1000,
  "excluded_policy_types": ["regulation"]
}
```

**Response:**
```json
{
  "message": "Generated 5 policy recommendations",
  "recommendations": [
    {
      "id": 1,
      "title": "Bus Lane Expansion",
      "description": "Expand dedicated bus lanes...",
      "rationale": "Addresses high traffic congestion...",
      "recommendation_type": "quick_win",
      "priority_score": 0.85,
      "expected_outcomes": {
        "co2_reduction_tonnes": 500,
        "travel_time_reduction_minutes": 10,
        "equity_score": 0.8
      },
      "confidence_score": 0.9,
      "estimated_cost": 5000000,
      "implementation_difficulty": "medium",
      "timeline_months": 12
    }
  ]
}
```

### Optimize Policy Package

```http
POST /policies/optimize/{city_id}
```

**Request Body:** Same as policy recommendations

**Response:**
```json
{
  "message": "Generated optimized policy package",
  "package": {
    "id": 1,
    "name": "Optimized Policy Package for San Francisco",
    "description": "AI-optimized combination of policies for maximum impact",
    "total_cost": 15000000,
    "implementation_timeline_months": 18,
    "expected_benefits": {
      "total_co2_reduction_tonnes": 2500,
      "total_cost": 15000000,
      "average_equity_score": 0.75,
      "policy_count": 3,
      "estimated_roi": 16.7
    },
    "status": "draft"
  }
}
```

## Simulations API

### Get Simulations

```http
GET /simulations
```

**Query Parameters:**
- `city_id` (int): Filter by city
- `status` (string): Filter by status

### Create Simulation

```http
POST /simulations
```

**Request Body:**
```json
{
  "city_id": 1,
  "policy_id": 1,
  "name": "Bus Lane Impact Simulation",
  "description": "Simulate the impact of bus lane expansion on traffic and emissions",
  "simulation_type": "policy_test",
  "parameters": {
    "weather_conditions": "normal",
    "traffic_patterns": "rush_hour"
  },
  "timesteps": 1000,
  "agent_count": 5000
}
```

### Run Simulation

```http
POST /simulations/{simulation_id}/run
```

**Response:**
```json
{
  "message": "Simulation started",
  "simulation_id": 1
}
```

### Get Simulation Results

```http
GET /simulations/{simulation_id}/results
```

**Response:**
```json
{
  "simulation_id": 1,
  "results": {
    "total_co2_emissions": 1250.5,
    "total_energy_consumption": 5000.2,
    "avg_travel_time": 22.5,
    "modal_split": {
      "car": 55.0,
      "transit": 30.0,
      "bike": 10.0,
      "walk": 5.0
    }
  },
  "metrics": {
    "total_agents": 5000,
    "total_timesteps": 1000,
    "total_co2_emissions": 1250.5,
    "total_energy_consumption": 5000.2,
    "avg_travel_time": 22.5,
    "modal_split": {...}
  },
  "status": "completed",
  "progress_percent": 100.0
}
```

## Predictions API

### Get Prediction Models

```http
GET /predictions/models
```

### Create Prediction Model

```http
POST /predictions/models
```

**Request Body:**
```json
{
  "name": "Travel Time Prediction Model",
  "description": "Predicts travel time based on traffic conditions",
  "model_type": "regression",
  "target_variable": "travel_time_minutes",
  "algorithm": "random_forest",
  "model_config": {
    "n_estimators": 100,
    "max_depth": 10
  },
  "feature_columns": ["congestion_level", "time_of_day", "weather"],
  "version": "1.0.0"
}
```

### Make Prediction

```http
POST /predictions/predict/{model_id}
```

**Request Body:**
```json
{
  "congestion_level": 0.7,
  "time_of_day": 8.5,
  "weather": "clear"
}
```

**Response:**
```json
{
  "model_id": 1,
  "input_data": {...},
  "prediction": {
    "predicted_value": 25.5,
    "confidence_interval": {
      "lower": 22.1,
      "upper": 28.9
    },
    "prediction_probability": 0.85
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Data Upload API

### Upload Mobility Data

```http
POST /data/upload/mobility/{city_id}
```

**Request:** Multipart form data with CSV file

**Response:**
```json
{
  "message": "Successfully uploaded 100 mobility data records",
  "city_id": 1,
  "records_created": 100
}
```

### Upload Air Quality Data

```http
POST /data/upload/air-quality/{city_id}
```

### Upload Energy Data

```http
POST /data/upload/energy/{city_id}
```

### Export City Data

```http
GET /data/export/{city_id}
```

**Query Parameters:**
- `data_type` (string): mobility, air-quality, or energy
- `start_date` (datetime): Start date filter
- `end_date` (datetime): End date filter

**Response:**
```json
{
  "message": "Exported 100 mobility records",
  "city_id": 1,
  "data_type": "mobility",
  "record_count": 100,
  "csv_content": "timestamp,avg_travel_time_minutes,..."
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

## Rate Limiting

API requests are rate limited to:
- 1000 requests per hour per IP
- 100 requests per minute per IP

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Webhooks

The API supports webhooks for simulation completion:

```http
POST /webhooks/simulation-complete
```

**Request Body:**
```json
{
  "simulation_id": 1,
  "status": "completed",
  "results": {...},
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## SDKs

Official SDKs are available for:
- Python: `pip install sustainable-cities-sdk`
- JavaScript: `npm install sustainable-cities-sdk`
- R: `install.packages("sustainableCities")`

## Support

For API support:
- Documentation: [API Docs](https://docs.sustainable-cities.com)
- Support: support@sustainable-cities.com
- GitHub Issues: [Project Repository](https://github.com/your-org/sustainable-cities-planner)
