#!/bin/bash

# AI Sustainable Cities Planner - CloudShell Deployment Script
echo "🚀 Starting AI Sustainable Cities Planner Deployment..."

# Set variables
AWS_REGION="us-east-1"
ECR_REPO="sustainable-cities-backend"
ECR_URI="061309713243.dkr.ecr.us-east-1.amazonaws.com/$ECR_REPO"

# Create project directory
mkdir -p sustainable-cities-planner
cd sustainable-cities-planner

echo "📁 Creating project structure..."

# Create backend directory
mkdir -p backend/app/{core,models,api/v1/endpoints,schemas,simulation,policy}
mkdir -p frontend/src/{components,pages,services}

echo "📝 Creating backend files..."

# Backend main.py
cat > backend/app/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
    return {"message": "AI Sustainable Cities Planner API", "status": "running"}

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
                "air_quality_index": 45
            },
            {
                "id": 2,
                "name": "Portland",
                "population": 652503,
                "area_km2": 376.5,
                "emissions_tonnes_co2": 1800000,
                "air_quality_index": 35
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
                "co2_reduction_percent": 15
            },
            {
                "id": 2,
                "name": "EV Charging Infrastructure",
                "type": "energy",
                "description": "Install 1000 new EV charging stations across the city",
                "estimated_cost": 25000000,
                "co2_reduction_percent": 8
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
                "results": {
                    "travel_time_reduction": 12,
                    "emissions_reduction": 18,
                    "cost_benefit_ratio": 2.3
                }
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Backend requirements.txt
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.2
matplotlib==3.7.2
seaborn==0.12.2
requests==2.31.0
python-dotenv==1.0.0
EOF

# Backend Dockerfile
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

echo "🐳 Building Docker image..."

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

# Build the image
docker build -t $ECR_REPO ./backend

# Tag the image
docker tag $ECR_REPO:latest $ECR_URI:latest

echo "📤 Pushing image to ECR..."

# Push the image
docker push $ECR_URI:latest

echo "✅ Image pushed successfully!"
echo "🌐 Your application will be available at:"
echo "   http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com"

echo "🔄 Updating ECS service to use the new image..."

# Force new deployment
aws ecs update-service \
    --cluster prod-sus-cities-cluster \
    --service prod-sus-cities-service \
    --force-new-deployment \
    --region $AWS_REGION

echo "🎉 Deployment complete!"
echo "⏳ Please wait 2-3 minutes for the service to start..."
echo "🔍 Check service status with:"
echo "   aws ecs describe-services --cluster prod-sus-cities-cluster --services prod-sus-cities-service --region $AWS_REGION"
