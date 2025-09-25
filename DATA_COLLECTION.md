# City Data Collection System

## Overview
The AI Sustainable Cities Planner collects data from multiple sources to provide comprehensive city analysis and policy recommendations. The system combines static baseline data with real-time API integrations.

## Data Sources & Collection Methods

### 1. **Static City Data (Frontend)**
**Location:** `frontend/src/App.js` (lines 27-59)

**Data Collected:**
- City names (30+ Michigan cities)
- Population estimates
- Annual CO₂ emissions
- Sustainability scores (0-100)
- State information

**Data Sources:**
- US Census Bureau population data
- EPA emissions inventories
- City sustainability reports
- Academic research papers

**Update Frequency:** Manual updates (quarterly/annual)

### 2. **Real-Time Air Quality Data**
**Location:** `backend/app/services/air_quality.py`

**APIs Integrated:**
- **OpenWeatherMap Air Pollution API**
  - Current AQI (Air Quality Index)
  - PM2.5, PM10, O₃, NO₂, SO₂, CO levels
  - Update frequency: Every 10 minutes
  - Coverage: Global

- **AirVisual API (IQAir)**
  - Historical air quality data
  - Forecast data (5 days)
  - Update frequency: Hourly
  - Coverage: 10,000+ cities

- **EPA AirNow API**
  - US-specific air quality data
  - Regulatory compliance data
  - Update frequency: Hourly
  - Coverage: US cities

**Data Collection Intervals:**
- Current conditions: Every 10 minutes
- Historical data: Daily
- Forecasts: Every 6 hours

### 3. **Real-Time Transportation Data**
**Location:** `backend/app/services/transportation.py`

**APIs Integrated:**
- **HERE Traffic API**
  - Real-time traffic flow
  - Congestion levels
  - Travel time estimates
  - Update frequency: Every 2 minutes

- **Google Maps API**
  - Traffic conditions
  - Route optimization
  - Public transit data
  - Update frequency: Real-time

- **City Transit APIs (GTFS)**
  - Bus/train schedules
  - Real-time arrivals
  - Service disruptions
  - Update frequency: Every 30 seconds

**Data Collection Intervals:**
- Traffic data: Every 2 minutes
- Transit data: Every 30 seconds
- Route data: On-demand

### 4. **Real-Time Energy Data**
**Location:** `backend/app/services/energy.py`

**APIs Integrated:**
- **EIA (Energy Information Administration)**
  - Energy consumption data
  - Renewable energy statistics
  - Grid reliability metrics
  - Update frequency: Monthly

- **EPA Power Profiler**
  - Emissions factors
  - Energy mix data
  - Update frequency: Annual

- **City Utility APIs**
  - Real-time consumption
  - Smart grid data
  - Update frequency: Every 15 minutes

**Data Collection Intervals:**
- Real-time consumption: Every 15 minutes
- Grid data: Every 5 minutes
- Historical data: Monthly

## Data Processing Pipeline

### 1. **Data Ingestion**
```
Real-time APIs → Data Validation → Database Storage → Cache Layer
```

### 2. **Data Validation**
- Range checks for all metrics
- Outlier detection
- Data quality scoring
- Missing data handling

### 3. **Data Storage**
- **PostgreSQL:** Structured data (cities, policies, simulations)
- **Redis:** Real-time data cache
- **S3:** Historical data archives

### 4. **Data Updates**
- **Real-time:** Air quality, traffic, energy consumption
- **Hourly:** Transit schedules, weather data
- **Daily:** Historical trends, policy impacts
- **Weekly:** City rankings, sustainability scores
- **Monthly:** Comprehensive reports

## Data Quality & Accuracy

### **Accuracy Levels:**
- **Population Data:** 95%+ (Census Bureau)
- **Emissions Data:** 90%+ (EPA verified)
- **Air Quality:** 98%+ (EPA certified sensors)
- **Traffic Data:** 85%+ (GPS + sensors)
- **Energy Data:** 92%+ (Utility company data)

### **Data Validation:**
- Cross-reference multiple sources
- Statistical outlier detection
- Temporal consistency checks
- Geographic boundary validation

## Privacy & Security

### **Data Protection:**
- No personal information collected
- Aggregated city-level data only
- API keys encrypted and rotated
- GDPR/CCPA compliant

### **Data Retention:**
- Real-time data: 30 days
- Historical data: 5 years
- Analytics data: 2 years
- Backup data: 7 years

## API Rate Limits & Costs

### **OpenWeatherMap:**
- Free tier: 1,000 calls/day
- Paid tier: 1,000,000 calls/month
- Cost: $0.0015 per call

### **HERE API:**
- Free tier: 250,000 transactions/month
- Paid tier: $0.50 per 1,000 transactions

### **Google Maps:**
- Free tier: $200 credit/month
- Traffic data: $0.005 per request

### **EIA API:**
- Free tier: 5,000 calls/day
- No paid tiers available

## Data Collection Schedule

### **Daily Operations:**
```
00:00 - Historical data backup
00:30 - Air quality data collection
01:00 - Energy consumption update
01:30 - Traffic pattern analysis
02:00 - Transit schedule update
...
23:30 - Final data validation
```

### **Weekly Operations:**
- Monday: City sustainability score updates
- Wednesday: Policy impact analysis
- Friday: Comprehensive data quality report
- Sunday: System maintenance and optimization

## Future Enhancements

### **Planned Integrations:**
1. **IoT Sensors:** Direct city sensor data
2. **Satellite Data:** Remote sensing for air quality
3. **Social Media:** Public sentiment analysis
4. **Economic Data:** GDP, employment statistics
5. **Health Data:** Public health indicators

### **Advanced Analytics:**
- Machine learning predictions
- Anomaly detection
- Trend analysis
- Policy impact modeling

## Monitoring & Alerts

### **Data Quality Monitoring:**
- API response time tracking
- Data freshness alerts
- Missing data notifications
- Accuracy threshold monitoring

### **System Health:**
- Database performance metrics
- API rate limit monitoring
- Error rate tracking
- Uptime monitoring

## Contact & Support

For questions about data collection:
- **Technical Issues:** Check system logs
- **Data Accuracy:** Review validation reports
- **API Integration:** Contact development team
- **Privacy Concerns:** Review privacy policy

---

*Last Updated: September 2024*
*Next Review: December 2024*
