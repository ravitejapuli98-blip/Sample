#!/bin/bash

# AI Sustainable Cities Planner - ECR Deployment Script
echo "🚀 Starting ECR deployment for AI Sustainable Cities Planner..."

# Set variables
AWS_REGION="us-east-1"
ECR_REPO="sustainable-cities-backend"
ECR_URI="061309713243.dkr.ecr.us-east-1.amazonaws.com/$ECR_REPO"

# Create project directory
mkdir -p sustainable-cities-deploy
cd sustainable-cities-deploy

echo "📁 Creating application files..."

# Create a simple FastAPI application
cat > app.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="AI Sustainable Cities Planner",
    description="Multi-agent simulation and planning tool for sustainable urban development",
    version="1.0.0"
)

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
                "emissions_tonnes_co2": 2500000,
                "air_quality_index": 45,
                "sustainability_score": 78
            },
            {
                "id": 2,
                "name": "Portland",
                "population": 652503,
                "emissions_tonnes_co2": 1800000,
                "air_quality_index": 35,
                "sustainability_score": 85
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

# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
requests==2.31.0
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
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
COPY app.py .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

echo "🐳 Building Docker image..."

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

# Build the image
docker build -t $ECR_REPO .

# Tag the image
docker tag $ECR_REPO:latest $ECR_URI:latest

echo "📤 Pushing image to ECR..."

# Push the image
docker push $ECR_URI:latest

echo "🔄 Updating ECS service..."

# Force new deployment
aws ecs update-service \
    --cluster prod-sus-cities-cluster \
    --service prod-sus-cities-service \
    --force-new-deployment \
    --region $AWS_REGION

echo "✅ Deployment complete!"
echo "🌐 Your AI Sustainable Cities Planner is now available at:"
echo "   http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com"
echo "⏳ Please wait 2-3 minutes for the service to start..."
echo ""
echo "🔗 Test these endpoints:"
echo "   - http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com/health"
echo "   - http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com/api/v1/cities"
echo "   - http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com/api/v1/policies"
