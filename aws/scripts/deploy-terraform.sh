#!/bin/bash

# AI Sustainable Cities Planner - Terraform Deployment Script
set -e

# Configuration
ENVIRONMENT=${1:-production}
REGION=${2:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
REPO_NAME="sustainable-cities-backend"

echo "🚀 Deploying AI Sustainable Cities Planner with Terraform"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo "Account ID: $ACCOUNT_ID"

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not installed. Please install Terraform first."
    exit 1
fi

# Initialize Terraform
echo "🔧 Initializing Terraform..."
cd terraform
terraform init

# Create ECR repository if it doesn't exist
echo "📦 Setting up ECR repository..."
aws ecr describe-repositories --repository-names $REPO_NAME --region $REGION > /dev/null 2>&1 || \
aws ecr create-repository --repository-name $REPO_NAME --region $REGION

# Get ECR login token
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Build and push Docker image
echo "🏗️ Building and pushing Docker image..."
cd ../backend
docker build -t $REPO_NAME:latest .
docker tag $REPO_NAME:latest $ECR_REGISTRY/$REPO_NAME:latest
docker push $ECR_REGISTRY/$REPO_NAME:latest
cd ../terraform

# Plan Terraform deployment
echo "📋 Planning Terraform deployment..."
terraform plan \
    -var="environment=$ENVIRONMENT" \
    -var="aws_region=$REGION" \
    -out=tfplan

# Apply Terraform deployment
echo "🏗️ Applying Terraform deployment..."
terraform apply tfplan

# Get outputs
echo "📋 Getting deployment outputs..."
CLUSTER_NAME=$(terraform output -raw ecs_cluster_name)
ALB_DNS=$(terraform output -raw load_balancer_dns)
DB_ENDPOINT=$(terraform output -raw database_endpoint)
REDIS_ENDPOINT=$(terraform output -raw redis_endpoint)

# Run database migrations
echo "🗄️ Running database migrations..."
TASK_ARN=$(aws ecs run-task \
    --cluster $CLUSTER_NAME \
    --task-definition $(terraform output -raw ecs_task_definition_arn | cut -d'/' -f2) \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$(terraform output -raw private_subnet_ids | jq -r '.[0]')],securityGroups=[$(terraform output -raw ecs_security_group_id)],assignPublicIp=ENABLED}" \
    --overrides '{"containerOverrides":[{"name":"backend-api","command":["python","-m","alembic","upgrade","head"]}]}' \
    --region $REGION \
    --query 'tasks[0].taskArn' \
    --output text)

# Wait for migration task to complete
echo "⏳ Waiting for database migrations to complete..."
aws ecs wait tasks-stopped \
    --cluster $CLUSTER_NAME \
    --tasks $TASK_ARN \
    --region $REGION

# Check migration task status
TASK_STATUS=$(aws ecs describe-tasks \
    --cluster $CLUSTER_NAME \
    --tasks $TASK_ARN \
    --region $REGION \
    --query 'tasks[0].lastStatus' \
    --output text)

if [ "$TASK_STATUS" = "STOPPED" ]; then
    EXIT_CODE=$(aws ecs describe-tasks \
        --cluster $CLUSTER_NAME \
        --tasks $TASK_ARN \
        --region $REGION \
        --query 'tasks[0].containers[0].exitCode' \
        --output text)
    
    if [ "$EXIT_CODE" = "0" ]; then
        echo "✅ Database migrations completed successfully"
    else
        echo "❌ Database migrations failed with exit code $EXIT_CODE"
        exit 1
    fi
else
    echo "❌ Database migration task did not complete properly"
    exit 1
fi

# Clean up
rm -f tfplan

echo "✅ Deployment completed successfully!"
echo "🌐 Application URL: http://$ALB_DNS"
echo "📊 ECS Cluster: $CLUSTER_NAME"
echo "🗄️ Database Endpoint: $DB_ENDPOINT"
echo "🔴 Redis Endpoint: $REDIS_ENDPOINT"

echo ""
echo "🎉 AI Sustainable Cities Planner is now running on AWS ECS!"
echo ""
echo "Next steps:"
echo "1. Configure your domain name to point to the ALB DNS: $ALB_DNS"
echo "2. Set up SSL certificate for HTTPS"
echo "3. Configure monitoring and alerting"
echo "4. Set up CI/CD pipeline for automated deployments"
