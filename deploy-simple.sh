#!/bin/bash

# Simple deployment script for AI Sustainable Cities Planner
echo "🚀 Starting simple deployment..."

# Set variables
AWS_REGION="us-east-1"
ECR_REPO="sustainable-cities-backend"
ECR_URI="061309713243.dkr.ecr.us-east-1.amazonaws.com/$ECR_REPO"

# Login to ECR
echo "🔐 Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

# Build the image
echo "🐳 Building Docker image..."
docker build -f Dockerfile.nginx -t $ECR_REPO .

# Tag the image
echo "🏷️ Tagging image..."
docker tag $ECR_REPO:latest $ECR_URI:latest

# Push the image
echo "📤 Pushing image to ECR..."
docker push $ECR_URI:latest

# Update ECS service
echo "🔄 Updating ECS service..."
aws ecs update-service \
    --cluster prod-sus-cities-cluster \
    --service prod-sus-cities-service \
    --force-new-deployment \
    --region $AWS_REGION

echo "✅ Deployment complete!"
echo "🌐 Your application is available at:"
echo "   http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com"
echo "⏳ Please wait 2-3 minutes for the service to start..."
