#!/bin/bash

# AI Sustainable Cities Planner - AWS Deployment Script
set -e

# Configuration
ENVIRONMENT=${1:-production}
REGION=${2:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
REPO_NAME="sustainable-cities-backend"

echo "🚀 Deploying AI Sustainable Cities Planner to AWS"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo "Account ID: $ACCOUNT_ID"

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Create ECR repository if it doesn't exist
echo "📦 Setting up ECR repository..."
aws ecr describe-repositories --repository-names $REPO_NAME --region $REGION > /dev/null 2>&1 || \
aws ecr create-repository --repository-name $REPO_NAME --region $REGION

# Get ECR login token
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Build and push Docker image
echo "🏗️ Building and pushing Docker image..."
cd backend
docker build -t $REPO_NAME:latest .
docker tag $REPO_NAME:latest $ECR_REGISTRY/$REPO_NAME:latest
docker push $ECR_REGISTRY/$REPO_NAME:latest
cd ..

# Deploy infrastructure with CloudFormation
echo "🏗️ Deploying infrastructure..."
aws cloudformation deploy \
    --template-file aws/cloudformation/infrastructure.yaml \
    --stack-name sustainable-cities-$ENVIRONMENT \
    --parameter-overrides \
        Environment=$ENVIRONMENT \
        DatabasePassword=$(openssl rand -base64 32) \
    --capabilities CAPABILITY_IAM \
    --region $REGION

# Get stack outputs
echo "📋 Getting stack outputs..."
CLUSTER_NAME=$(aws cloudformation describe-stacks \
    --stack-name sustainable-cities-$ENVIRONMENT \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`ECSClusterName`].OutputValue' \
    --output text)

ALB_DNS=$(aws cloudformation describe-stacks \
    --stack-name sustainable-cities-$ENVIRONMENT \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
    --output text)

# Update task definition with actual image URI
echo "📝 Updating task definition..."
sed "s/ACCOUNT_ID/$ACCOUNT_ID/g; s/REGION/$REGION/g" aws/ecs-task-definition.json > aws/ecs-task-definition-updated.json

# Register task definition
echo "📋 Registering task definition..."
TASK_DEFINITION_ARN=$(aws ecs register-task-definition \
    --cli-input-json file://aws/ecs-task-definition-updated.json \
    --region $REGION \
    --query 'taskDefinition.taskDefinitionArn' \
    --output text)

# Update service
echo "🔄 Updating ECS service..."
aws ecs update-service \
    --cluster $CLUSTER_NAME \
    --service sustainable-cities-planner-service \
    --task-definition $TASK_DEFINITION_ARN \
    --region $REGION > /dev/null || \
aws ecs create-service \
    --cluster $CLUSTER_NAME \
    --service-name sustainable-cities-planner-service \
    --task-definition $TASK_DEFINITION_ARN \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678,subnet-87654321],securityGroups=[sg-12345678],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:$REGION:$ACCOUNT_ID:targetgroup/sustainable-cities-tg/1234567890123456,containerName=backend-api,containerPort=8000" \
    --region $REGION

# Wait for service to stabilize
echo "⏳ Waiting for service to stabilize..."
aws ecs wait services-stable \
    --cluster $CLUSTER_NAME \
    --services sustainable-cities-planner-service \
    --region $REGION

# Run database migrations
echo "🗄️ Running database migrations..."
TASK_ARN=$(aws ecs run-task \
    --cluster $CLUSTER_NAME \
    --task-definition $TASK_DEFINITION_ARN \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678],securityGroups=[sg-12345678],assignPublicIp=ENABLED}" \
    --overrides '{"containerOverrides":[{"name":"backend-api","command":["python","-m","alembic","upgrade","head"]}]}' \
    --region $REGION \
    --query 'tasks[0].taskArn' \
    --output text)

# Wait for migration task to complete
aws ecs wait tasks-stopped \
    --cluster $CLUSTER_NAME \
    --tasks $TASK_ARN \
    --region $REGION

echo "✅ Deployment completed successfully!"
echo "🌐 Application URL: http://$ALB_DNS"
echo "📊 ECS Cluster: $CLUSTER_NAME"
echo "📋 Task Definition: $TASK_DEFINITION_ARN"

# Clean up temporary files
rm -f aws/ecs-task-definition-updated.json

echo "🎉 AI Sustainable Cities Planner is now running on AWS ECS!"
