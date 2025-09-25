# AI Sustainable Cities Planner

A multi-agent simulation and planning tool that ingests a city's mobility, air-quality, and energy data, then proposes policy packages and predicts outcomes for sustainable urban development.

## 🎯 Project Overview

**Elevator Pitch**: A policy "copilot" that uses AI to simulate urban policy impacts, helping cities make data-driven decisions for sustainable development.

### Key Features

- **Multi-Agent Simulation**: Simulates urban systems with realistic agent behaviors
- **Policy Optimization**: Recommends policy packages (bus lanes, EV charging, signal timing)
- **Outcome Prediction**: Predicts travel time, air quality (PM2.5), CO₂ emissions, grid load, and equity impact
- **Real-time Analysis**: Processes live city data for immediate insights
- **Interactive Dashboard**: Visual interface for policy exploration and scenario comparison

### Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Celery
- **AI/ML**: PyTorch, scikit-learn, NumPy, Pandas
- **Simulation**: Mesa (multi-agent modeling), NetworkX
- **Frontend**: React, TypeScript, D3.js, Mapbox
- **Database**: PostgreSQL, Redis
- **Deployment**: Docker, Kubernetes

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis 6+

### Installation

1. **Clone and setup backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Setup database**:
```bash
python -m alembic upgrade head
python scripts/seed_data.py
```

3. **Start backend services**:
```bash
python main.py
celery -A app.celery worker --loglevel=info
```

4. **Setup and start frontend**:
```bash
cd frontend
npm install
npm start
```

## 📊 Data Sources

The system integrates with various urban data sources:

- **Mobility**: Traffic sensors, public transit APIs, ride-sharing data
- **Air Quality**: EPA monitoring stations, satellite data
- **Energy**: Smart grid data, building energy consumption
- **Demographics**: Census data, economic indicators

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Simulation    │    │   Policy        │
│                 │    │   Engine        │    │   Engine        │
│ • Traffic APIs  │───▶│                 │───▶│                 │
│ • Air Quality   │    │ • Multi-Agent   │    │ • Optimization  │
│ • Energy Grid   │    │ • NetworkX      │    │ • ML Models     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                              │
│  • Data Ingestion  • Simulation API  • Policy Recommendations  │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    React Frontend                               │
│  • Interactive Maps  • Policy Dashboard  • Scenario Comparison  │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Use Cases

1. **Transportation Planning**: Optimize bus routes and bike lanes
2. **Air Quality Management**: Predict pollution reduction from EV adoption
3. **Energy Grid Planning**: Optimize EV charging station placement
4. **Equity Analysis**: Ensure policies benefit all communities
5. **Climate Action**: Model carbon reduction strategies

## 📈 Impact Metrics

- **Environmental**: CO₂ reduction, PM2.5 levels, energy efficiency
- **Social**: Travel time reduction, accessibility improvements
- **Economic**: Cost-benefit analysis, ROI calculations
- **Equity**: Distributional impacts across neighborhoods

## 🔬 Research Applications

Perfect for:
- Urban planning research
- Policy impact studies
- Climate action planning
- Transportation optimization
- Environmental justice analysis

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

We welcome contributions! Please see CONTRIBUTING.md for guidelines.

## 📞 Contact

For questions or collaboration opportunities, please open an issue or contact the development team.
