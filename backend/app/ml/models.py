"""
Machine Learning models for sustainable cities planning
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class PolicyImpactPredictor:
    """Predicts the impact of sustainability policies on cities"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_columns = [
            'population', 'area_km2', 'current_emissions', 'air_quality_index',
            'public_transit_usage', 'car_ownership_rate', 'bike_lane_km',
            'green_space_percent', 'energy_renewable_percent', 'building_efficiency'
        ]
        self.target_columns = [
            'emissions_reduction', 'air_quality_improvement', 'traffic_reduction',
            'energy_savings', 'cost_benefit_ratio'
        ]
        
    def generate_synthetic_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Generate synthetic training data for the models"""
        np.random.seed(42)
        
        data = {
            # City characteristics
            'population': np.random.normal(500000, 200000, n_samples),
            'area_km2': np.random.normal(300, 100, n_samples),
            'current_emissions': np.random.normal(2000000, 500000, n_samples),
            'air_quality_index': np.random.normal(50, 15, n_samples),
            'public_transit_usage': np.random.normal(25, 10, n_samples),
            'car_ownership_rate': np.random.normal(0.7, 0.1, n_samples),
            'bike_lane_km': np.random.normal(50, 20, n_samples),
            'green_space_percent': np.random.normal(15, 5, n_samples),
            'energy_renewable_percent': np.random.normal(20, 10, n_samples),
            'building_efficiency': np.random.normal(0.6, 0.1, n_samples),
            
            # Policy implementations (0-1 scale)
            'bus_lane_expansion': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'ev_charging_infrastructure': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            'green_building_standards': np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
            'bike_network_expansion': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            'renewable_energy_incentives': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        }
        
        df = pd.DataFrame(data)
        
        # Generate realistic target variables based on policy implementations
        df['emissions_reduction'] = (
            df['bus_lane_expansion'] * np.random.normal(15, 5, n_samples) +
            df['ev_charging_infrastructure'] * np.random.normal(8, 3, n_samples) +
            df['green_building_standards'] * np.random.normal(12, 4, n_samples) +
            df['bike_network_expansion'] * np.random.normal(5, 2, n_samples) +
            df['renewable_energy_incentives'] * np.random.normal(10, 3, n_samples) +
            np.random.normal(0, 2, n_samples)
        )
        
        df['air_quality_improvement'] = (
            df['emissions_reduction'] * 0.8 +
            df['green_space_percent'] * 0.1 +
            np.random.normal(0, 3, n_samples)
        )
        
        df['traffic_reduction'] = (
            df['bus_lane_expansion'] * np.random.normal(12, 4, n_samples) +
            df['bike_network_expansion'] * np.random.normal(8, 3, n_samples) +
            df['public_transit_usage'] * 0.2 +
            np.random.normal(0, 2, n_samples)
        )
        
        df['energy_savings'] = (
            df['green_building_standards'] * np.random.normal(15, 5, n_samples) +
            df['renewable_energy_incentives'] * np.random.normal(20, 6, n_samples) +
            df['building_efficiency'] * 10 +
            np.random.normal(0, 3, n_samples)
        )
        
        df['cost_benefit_ratio'] = (
            df['emissions_reduction'] * 0.1 +
            df['energy_savings'] * 0.05 +
            np.random.normal(2.0, 0.5, n_samples)
        )
        
        # Ensure positive values
        for col in self.target_columns:
            df[col] = np.maximum(df[col], 0)
        
        return df
    
    def train_models(self) -> Dict[str, Dict[str, float]]:
        """Train ML models for policy impact prediction"""
        logger.info("Generating synthetic training data...")
        df = self.generate_synthetic_data(2000)
        
        # Prepare features and targets
        feature_cols = self.feature_columns + [
            'bus_lane_expansion', 'ev_charging_infrastructure', 
            'green_building_standards', 'bike_network_expansion',
            'renewable_energy_incentives'
        ]
        
        X = df[feature_cols]
        y = df[self.target_columns]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        self.scalers['features'] = scaler
        
        # Train models for each target
        results = {}
        
        for i, target in enumerate(self.target_columns):
            logger.info(f"Training model for {target}...")
            
            # Random Forest
            rf_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            rf_model.fit(X_train_scaled, y_train.iloc[:, i])
            
            # Gradient Boosting
            gb_model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            gb_model.fit(X_train_scaled, y_train.iloc[:, i])
            
            # Linear Regression
            lr_model = LinearRegression()
            lr_model.fit(X_train_scaled, y_train.iloc[:, i])
            
            # Evaluate models
            rf_pred = rf_model.predict(X_test_scaled)
            gb_pred = gb_model.predict(X_test_scaled)
            lr_pred = lr_model.predict(X_test_scaled)
            
            rf_r2 = r2_score(y_test.iloc[:, i], rf_pred)
            gb_r2 = r2_score(y_test.iloc[:, i], gb_pred)
            lr_r2 = r2_score(y_test.iloc[:, i], lr_pred)
            
            # Choose best model
            if rf_r2 >= gb_r2 and rf_r2 >= lr_r2:
                best_model = rf_model
                best_r2 = rf_r2
                model_type = 'RandomForest'
            elif gb_r2 >= lr_r2:
                best_model = gb_model
                best_r2 = gb_r2
                model_type = 'GradientBoosting'
            else:
                best_model = lr_model
                best_r2 = lr_r2
                model_type = 'LinearRegression'
            
            self.models[target] = best_model
            
            results[target] = {
                'model_type': model_type,
                'r2_score': best_r2,
                'rmse': np.sqrt(mean_squared_error(y_test.iloc[:, i], best_model.predict(X_test_scaled)))
            }
            
            logger.info(f"{target}: {model_type} - R² = {best_r2:.3f}")
        
        return results
    
    def predict_policy_impact(self, city_data: Dict[str, Any], 
                            policies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict the impact of implementing specific policies"""
        
        if not self.models:
            logger.warning("Models not trained. Training now...")
            self.train_models()
        
        # Prepare input features
        features = np.array([
            city_data.get('population', 500000),
            city_data.get('area_km2', 300),
            city_data.get('emissions_tonnes_co2', 2000000),
            city_data.get('air_quality_index', 50),
            city_data.get('public_transit_usage', 25),
            city_data.get('car_ownership_rate', 0.7),
            city_data.get('bike_lane_km', 50),
            city_data.get('green_space_percent', 15),
            city_data.get('energy_renewable_percent', 20),
            city_data.get('building_efficiency', 0.6),
        ])
        
        # Add policy features
        policy_features = np.zeros(5)
        policy_names = [
            'bus_lane_expansion', 'ev_charging_infrastructure',
            'green_building_standards', 'bike_network_expansion',
            'renewable_energy_incentives'
        ]
        
        for policy in policies:
            policy_type = policy.get('type', '').lower()
            if 'transportation' in policy_type or 'bus' in policy_type:
                policy_features[0] = 1
            elif 'energy' in policy_type or 'ev' in policy_type:
                policy_features[1] = 1
            elif 'construction' in policy_type or 'building' in policy_type:
                policy_features[2] = 1
            elif 'bike' in policy_type or 'cycling' in policy_type:
                policy_features[3] = 1
            elif 'renewable' in policy_type or 'solar' in policy_type:
                policy_features[4] = 1
        
        # Combine features
        input_features = np.concatenate([features, policy_features]).reshape(1, -1)
        
        # Scale features
        input_features_scaled = self.scalers['features'].transform(input_features)
        
        # Make predictions
        predictions = {}
        for target, model in self.models.items():
            pred = model.predict(input_features_scaled)[0]
            predictions[target] = max(0, pred)  # Ensure non-negative
        
        # Calculate additional metrics
        total_impact = sum(predictions.values())
        cost_effectiveness = predictions['cost_benefit_ratio']
        
        return {
            'predictions': predictions,
            'total_impact_score': total_impact,
            'cost_effectiveness': cost_effectiveness,
            'recommended_policies': self._recommend_policies(predictions, policies),
            'confidence_score': min(0.95, total_impact / 100)  # Simple confidence metric
        }
    
    def _recommend_policies(self, predictions: Dict[str, float], 
                          implemented_policies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommend additional policies based on predictions"""
        recommendations = []
        
        if predictions['emissions_reduction'] < 20:
            recommendations.append({
                'type': 'transportation',
                'name': 'Enhanced Public Transit',
                'description': 'Expand bus rapid transit and metro systems',
                'expected_impact': 'High emissions reduction'
            })
        
        if predictions['air_quality_improvement'] < 15:
            recommendations.append({
                'type': 'environmental',
                'name': 'Green Infrastructure',
                'description': 'Increase urban green spaces and tree canopy',
                'expected_impact': 'Improved air quality'
            })
        
        if predictions['traffic_reduction'] < 10:
            recommendations.append({
                'type': 'transportation',
                'name': 'Smart Traffic Management',
                'description': 'Implement adaptive traffic signals and congestion pricing',
                'expected_impact': 'Reduced traffic congestion'
            })
        
        return recommendations

class CitySimilarityEngine:
    """Finds similar cities for benchmarking and recommendations"""
    
    def __init__(self):
        self.city_features = [
            'population', 'area_km2', 'emissions_tonnes_co2', 'air_quality_index',
            'public_transit_usage', 'car_ownership_rate', 'bike_lane_km',
            'green_space_percent', 'energy_renewable_percent', 'building_efficiency'
        ]
    
    def find_similar_cities(self, target_city: Dict[str, Any], 
                          city_database: List[Dict[str, Any]], 
                          n_similar: int = 5) -> List[Dict[str, Any]]:
        """Find cities similar to the target city"""
        
        if not city_database:
            return []
        
        # Prepare target city features
        target_features = np.array([
            target_city.get(feature, 0) for feature in self.city_features
        ])
        
        similarities = []
        
        for city in city_database:
            city_features = np.array([
                city.get(feature, 0) for feature in self.city_features
            ])
            
            # Calculate cosine similarity
            similarity = np.dot(target_features, city_features) / (
                np.linalg.norm(target_features) * np.linalg.norm(city_features)
            )
            
            similarities.append({
                'city': city,
                'similarity_score': similarity
            })
        
        # Sort by similarity and return top N
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similarities[:n_similar]

# Global instances
policy_predictor = PolicyImpactPredictor()
city_similarity_engine = CitySimilarityEngine()
