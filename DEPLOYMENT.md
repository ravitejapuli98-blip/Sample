# AI Sustainable Cities Planner - Deployment Guide

This guide covers deploying the AI Sustainable Cities Planner on AWS using Terraform and ECS Fargate.

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0 installed
- Docker installed
- jq for JSON processing (optional but recommended)

## Quick Start

### 1. Configure AWS CLI

```bash
aws configure
```

### 2. Set up Terraform Backend (Optional)

Create an S3 bucket for Terraform state:

```bash
aws s3 mb s3://your-terraform-state-bucket
```

Update `terraform/main.tf` with your bucket details.

### 3. Configure Variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 4. Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="environment=production"

# Apply infrastructure
terraform apply -var="environment=production"
```

### 5. Deploy Application

```bash
# Build and push Docker images
cd ..
./aws/scripts/deploy-terraform.sh production us-east-1
```

## Environment-Specific Deployments

### Development Environment

```bash
terraform apply -var="environment=development" \
  -var="ecs_desired_count=1" \
  -var="db_instance_class=db.t3.micro" \
  -var="use_fargate_spot=true"
```

### Production Environment

```bash
terraform apply -var="environment=production" \
  -var="ecs_desired_count=3" \
  -var="db_instance_class=db.r5.large" \
  -var="enable_auto_scaling=true"
```

## Configuration

### Environment Variables

Set these in your `terraform.tfvars`:

```hcl
# Required
aws_region = "us-east-1"
environment = "production"

# Database
db_instance_class = "db.t3.medium"
db_allocated_storage = 100

# ECS
ecs_task_cpu = 2048
ecs_task_memory = 4096
ecs_desired_count = 2

# Secrets (set via environment variables)
export TF_VAR_openweather_api_key="your-api-key"
export TF_VAR_google_maps_api_key="your-api-key"
export TF_VAR_database_password="your-secure-password"
```

### API Keys

The application requires API keys for external data sources:

1. **OpenWeather API**: Get from [OpenWeatherMap](https://openweathermap.org/api)
2. **Google Maps API**: Get from [Google Cloud Console](https://console.cloud.google.com/)

## Monitoring and Logging

### CloudWatch Logs

- Application logs: `/ecs/{environment}-sustainable-cities-planner`
- Database logs: RDS logs in CloudWatch
- Load balancer logs: ALB access logs

### Container Insights

ECS Container Insights is enabled by default for monitoring:
- CPU and memory utilization
- Task count and health
- Network metrics

### Health Checks

- Application: `GET /health`
- Database: RDS health checks
- Load balancer: Target group health checks

## Scaling

### Auto Scaling

ECS auto scaling is configured based on CPU utilization:

```hcl
# In terraform/variables.tf
enable_auto_scaling = true
ecs_min_capacity = 1
ecs_max_capacity = 10
```

### Manual Scaling

```bash
# Update desired count
aws ecs update-service \
  --cluster production-sustainable-cities-cluster \
  --service production-sustainable-cities-service \
  --desired-count 5
```

## Security

### Network Security

- VPC with public/private subnets
- Security groups with minimal required access
- NAT gateways for private subnet internet access

### Data Security

- RDS encryption at rest
- ElastiCache encryption in transit and at rest
- Secrets Manager for sensitive data
- IAM roles with least privilege

### SSL/TLS

For production, set up SSL certificates:

```bash
# Request certificate
aws acm request-certificate \
  --domain-name your-domain.com \
  --validation-method DNS

# Update ALB listener to use HTTPS
```

## Backup and Recovery

### Database Backups

RDS automated backups are enabled:
- Backup retention: 7 days (configurable)
- Backup window: 03:00-04:00 UTC
- Maintenance window: Sun 04:00-05:00 UTC

### Manual Backups

```bash
# Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier production-sustainable-cities-db \
  --db-snapshot-identifier manual-backup-$(date +%Y%m%d)
```

## Troubleshooting

### Common Issues

1. **ECS Tasks not starting**
   ```bash
   # Check task logs
   aws logs get-log-events \
     --log-group-name /ecs/production-sustainable-cities-planner \
     --log-stream-name backend/ecs-task-id
   ```

2. **Database connection issues**
   ```bash
   # Check RDS status
   aws rds describe-db-instances \
     --db-instance-identifier production-sustainable-cities-db
   ```

3. **Load balancer health checks failing**
   ```bash
   # Check target group health
   aws elbv2 describe-target-health \
     --target-group-arn your-target-group-arn
   ```

### Useful Commands

```bash
# View ECS service status
aws ecs describe-services \
  --cluster production-sustainable-cities-cluster \
  --services production-sustainable-cities-service

# Check application logs
aws logs tail /ecs/production-sustainable-cities-planner --follow

# Test database connectivity
aws rds describe-db-instances \
  --db-instance-identifier production-sustainable-cities-db
```

## Cost Optimization

### Fargate Spot

Use Fargate Spot for non-critical workloads:

```hcl
use_fargate_spot = true
```

### Reserved Instances

For predictable workloads, consider RDS Reserved Instances:

```bash
aws rds describe-reserved-db-instances-offerings
```

### S3 Lifecycle

Configure S3 lifecycle policies for data archival:

```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket your-bucket-name \
  --lifecycle-configuration file://lifecycle.json
```

## Cleanup

To destroy the infrastructure:

```bash
# Remove application data first
aws s3 rm s3://your-bucket-name --recursive

# Destroy Terraform infrastructure
terraform destroy -var="environment=production"
```

**Warning**: This will permanently delete all resources and data.

## Support

For deployment issues:

1. Check the troubleshooting section
2. Review CloudWatch logs
3. Open an issue in the project repository
4. Contact the development team
