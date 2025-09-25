# 🚀 AI Sustainable Cities Planner - GitHub Actions CI/CD Setup

## Overview
This repository now includes a complete CI/CD pipeline using GitHub Actions to automatically build and deploy your AI Sustainable Cities Planner to AWS ECS.

## 🛠️ Setup Instructions

### 1. Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `ai-sustainable-cities-planner`
3. Make it public or private (your choice)

### 2. Push Your Code
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit your code
git commit -m "Initial commit: AI Sustainable Cities Planner with CI/CD"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/ai-sustainable-cities-planner.git

# Push to GitHub
git push -u origin main
```

### 3. Configure GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `AWS_ACCESS_KEY_ID`: `YOUR_AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`: `YOUR_AWS_SECRET_ACCESS_KEY`

### 4. Trigger Deployment
The deployment will automatically trigger when you:
- Push to `main` or `master` branch
- Create a pull request
- Manually trigger via GitHub Actions tab

## 🔄 How It Works

### GitHub Actions Workflow
1. **Checkout Code**: Gets your latest code
2. **Configure AWS**: Sets up AWS credentials
3. **Login to ECR**: Authenticates with Amazon ECR
4. **Build Docker Image**: Creates your FastAPI application container
5. **Push to ECR**: Uploads image to your ECR repository
6. **Deploy to ECS**: Updates your ECS service with the new image
7. **Verify Deployment**: Confirms the deployment was successful

### What Gets Deployed
- ✅ **FastAPI Backend**: Complete AI Sustainable Cities Planner API
- ✅ **API Endpoints**: Cities, policies, simulations, predictions, analytics
- ✅ **Health Checks**: Monitoring and status endpoints
- ✅ **Auto-scaling**: ECS Fargate with load balancer
- ✅ **Logging**: CloudWatch integration

## 🌐 Your Application URLs

Once deployed, your application will be available at:
- **Main App**: http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com
- **Health Check**: http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com/health
- **API Documentation**: http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com/docs

## 📊 API Endpoints

### Core Endpoints
- `GET /` - Application info and available endpoints
- `GET /health` - Health check
- `GET /api/v1/cities` - City data and metrics
- `GET /api/v1/policies` - Policy recommendations
- `GET /api/v1/simulations` - Simulation results
- `GET /api/v1/predictions` - Outcome predictions
- `GET /api/v1/analytics` - Overall analytics

### Sample Data Included
- **3 Cities**: San Francisco, Portland, Seattle
- **4 Policies**: Bus lanes, EV charging, green buildings, smart traffic
- **3 Simulations**: Transportation, energy, comprehensive
- **3 Predictions**: Policy impact forecasts
- **Analytics**: Overall metrics and ROI

## 🔧 Customization

### Adding New Cities
Edit `backend/app/main.py` and add to the `get_cities()` function.

### Adding New Policies
Edit `backend/app/main.py` and add to the `get_policies()` function.

### Modifying Deployment
Edit `.github/workflows/deploy.yml` to change deployment settings.

## 🚨 Troubleshooting

### If Deployment Fails
1. Check GitHub Actions logs in the Actions tab
2. Verify AWS credentials are correct
3. Ensure ECR repository exists
4. Check ECS service status in AWS Console

### If Application Doesn't Load
1. Wait 2-3 minutes for ECS service to start
2. Check ECS service logs in CloudWatch
3. Verify load balancer health checks
4. Check security group rules

## 🎉 Success!

Once deployed, you'll have a fully functional AI Sustainable Cities Planner running on AWS with:
- ✅ Automatic deployments on code changes
- ✅ Scalable infrastructure
- ✅ Health monitoring
- ✅ API documentation
- ✅ Real-time analytics

Your application is now production-ready and will automatically update whenever you push new code to GitHub!
