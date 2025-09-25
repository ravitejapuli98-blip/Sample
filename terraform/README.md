# AI Sustainable Cities Planner - Terraform Infrastructure

This directory contains the Terraform configuration for deploying the AI Sustainable Cities Planner on AWS using ECS Fargate.

## Architecture Overview

The infrastructure includes:

- **VPC**: Multi-AZ VPC with public and private subnets
- **ECS Fargate**: Containerized application deployment
- **RDS PostgreSQL**: Managed database for application data
- **ElastiCache Redis**: Caching and task queue
- **Application Load Balancer**: Traffic distribution
- **ECR**: Container image registry
- **S3**: Application data storage
- **Secrets Manager**: API keys and sensitive data
- **CloudWatch**: Logging and monitoring

## Prerequisites

1. **AWS CLI** configured with appropriate permissions
2. **Terraform** >= 1.0 installed
3. **Docker** for building container images
4. **jq** for JSON processing (optional but recommended)

## Quick Start

1. **Copy and customize variables**:
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

2. **Initialize Terraform**:
```bash
cd terraform
terraform init
```

3. **Plan deployment**:
```bash
terraform plan -var="environment=production"
```

4. **Deploy infrastructure**:
```bash
terraform apply -var="environment=production"
```

5. **Deploy application**:
```bash
cd ..
./aws/scripts/deploy-terraform.sh production us-east-1
```

## Configuration

### Required Variables

- `aws_region`: AWS region for deployment
- `environment`: Environment name (development, staging, production)

### Optional Variables

See `terraform.tfvars.example` for all available configuration options.

### Secrets Management

API keys and sensitive data are managed through AWS Secrets Manager:

```bash
# Set secrets via Terraform variables
export TF_VAR_openweather_api_key="your-api-key"
export TF_VAR_google_maps_api_key="your-api-key"
export TF_VAR_database_password="your-secure-password"
```

## Infrastructure Components

### Networking
- VPC with public/private subnets across 2 AZs
- NAT Gateways for private subnet internet access
- Security groups for network isolation

### Compute
- ECS Fargate cluster with auto-scaling
- Application Load Balancer for traffic distribution
- Container Insights for monitoring

### Data
- RDS PostgreSQL with Multi-AZ for high availability
- ElastiCache Redis for caching and task queues
- S3 bucket for application data storage

### Security
- IAM roles with least privilege access
- Secrets Manager for sensitive data
- VPC endpoints for secure AWS service access

## Deployment Environments

### Development
```bash
terraform apply -var="environment=development" \
  -var="ecs_desired_count=1" \
  -var="db_instance_class=db.t3.micro" \
  -var="use_fargate_spot=true"
```

### Production
```bash
terraform apply -var="environment=production" \
  -var="ecs_desired_count=3" \
  -var="db_instance_class=db.r5.large" \
  -var="enable_auto_scaling=true"
```

## Monitoring and Logging

- **CloudWatch Logs**: Application and system logs
- **Container Insights**: ECS performance metrics
- **RDS Enhanced Monitoring**: Database performance
- **ALB Access Logs**: Request logging

## Cost Optimization

- **Fargate Spot**: Use spot instances for non-critical workloads
- **Auto Scaling**: Scale based on CPU/memory utilization
- **S3 Lifecycle**: Automatic data archival
- **RDS Reserved Instances**: For predictable workloads

## Security Best Practices

- Private subnets for application and database
- Security groups with minimal required access
- Secrets Manager for sensitive data
- VPC Flow Logs for network monitoring
- Encryption at rest and in transit

## Troubleshooting

### Common Issues

1. **ECS Tasks not starting**:
   - Check security group rules
   - Verify task definition parameters
   - Check CloudWatch logs

2. **Database connection issues**:
   - Verify RDS security group allows ECS access
   - Check database endpoint and credentials

3. **Load balancer health checks failing**:
   - Verify application is listening on correct port
   - Check health check path configuration

### Useful Commands

```bash
# View ECS service status
aws ecs describe-services --cluster <cluster-name> --services <service-name>

# Check task logs
aws logs get-log-events --log-group-name /ecs/<cluster-name> --log-stream-name <stream-name>

# Test database connectivity
aws rds describe-db-instances --db-instance-identifier <db-identifier>
```

## Cleanup

To destroy the infrastructure:

```bash
terraform destroy -var="environment=production"
```

**Warning**: This will permanently delete all resources and data.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review CloudWatch logs
3. Open an issue in the project repository
