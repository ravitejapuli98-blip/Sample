"""
Prediction models for ML-based outcome forecasting
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class PredictionModel(Base):
    """ML model for outcome prediction"""
    __tablename__ = "prediction_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Model metadata
    model_type = Column(String(50), nullable=False)  # regression, classification, time_series
    target_variable = Column(String(100), nullable=False)  # travel_time, co2_emissions, etc.
    algorithm = Column(String(50), nullable=False)  # random_forest, neural_network, etc.
    
    # Model configuration
    model_config = Column(JSON)  # Hyperparameters, architecture, etc.
    feature_columns = Column(JSON)  # List of input features
    
    # Performance metrics
    accuracy_score = Column(Float)
    r2_score = Column(Float)
    mae = Column(Float)  # Mean Absolute Error
    rmse = Column(Float)  # Root Mean Square Error
    
    # Model artifacts
    model_path = Column(String(500))  # Path to saved model file
    scaler_path = Column(String(500))  # Path to feature scaler
    feature_importance = Column(JSON)  # Feature importance scores
    
    # Training data
    training_data_size = Column(Integer)
    training_date_range = Column(JSON)  # {start: date, end: date}
    
    # Status
    status = Column(String(20), default="draft")  # draft, training, trained, deployed, archived
    version = Column(String(20), default="1.0.0")
    
    # Relationships
    predictions = relationship("Prediction", back_populates="model")
    model_evaluations = relationship("ModelEvaluation", back_populates="model")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Prediction(Base):
    """Individual predictions made by models"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("prediction_models.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True)
    
    # Prediction metadata
    prediction_type = Column(String(50), nullable=False)  # policy_impact, scenario_analysis, etc.
    time_horizon = Column(Integer)  # Prediction horizon in days/months/years
    
    # Input data
    input_features = Column(JSON)  # Features used for prediction
    input_data_hash = Column(String(64))  # Hash of input data for caching
    
    # Prediction results
    predicted_value = Column(Float)
    confidence_interval = Column(JSON)  # {lower: value, upper: value}
    prediction_probability = Column(Float)  # For classification models
    
    # Context
    prediction_context = Column(JSON)  # Additional context (weather, events, etc.)
    scenario_parameters = Column(JSON)  # Scenario-specific parameters
    
    # Validation
    actual_value = Column(Float)  # Actual observed value (for validation)
    prediction_error = Column(Float)  # Difference between predicted and actual
    is_validated = Column(Boolean, default=False)
    
    # Relationships
    model = relationship("PredictionModel", back_populates="predictions")
    city = relationship("City")
    policy = relationship("Policy")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ModelEvaluation(Base):
    """Model evaluation and validation results"""
    __tablename__ = "model_evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("prediction_models.id"), nullable=False)
    
    # Evaluation metadata
    evaluation_type = Column(String(50), nullable=False)  # cross_validation, holdout, temporal
    evaluation_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Dataset information
    test_data_size = Column(Integer)
    test_data_date_range = Column(JSON)
    
    # Performance metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    r2_score = Column(Float)
    mae = Column(Float)
    rmse = Column(Float)
    mape = Column(Float)  # Mean Absolute Percentage Error
    
    # Detailed metrics
    confusion_matrix = Column(JSON)  # For classification models
    roc_auc = Column(Float)  # For binary classification
    feature_importance = Column(JSON)
    
    # Validation results
    cross_validation_scores = Column(JSON)  # List of CV scores
    validation_plots = Column(JSON)  # Paths to validation plots
    
    # Relationships
    model = relationship("PredictionModel", back_populates="model_evaluations")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PredictionBatch(Base):
    """Batch prediction jobs"""
    __tablename__ = "prediction_batches"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Batch configuration
    model_ids = Column(JSON)  # List of model IDs to use
    input_data_source = Column(String(100))  # database, file, api
    input_data_config = Column(JSON)
    
    # Batch parameters
    batch_size = Column(Integer, default=1000)
    parallel_workers = Column(Integer, default=4)
    
    # Status and results
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    progress_percent = Column(Float, default=0.0)
    total_predictions = Column(Integer)
    completed_predictions = Column(Integer, default=0)
    
    # Results
    results_summary = Column(JSON)
    output_location = Column(String(500))  # Where results are stored
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PredictionCache(Base):
    """Cache for frequently requested predictions"""
    __tablename__ = "prediction_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Cache key
    cache_key = Column(String(255), nullable=False, unique=True, index=True)
    
    # Prediction data
    model_id = Column(Integer, ForeignKey("prediction_models.id"), nullable=False)
    input_hash = Column(String(64), nullable=False, index=True)
    
    # Cached results
    prediction_result = Column(JSON)
    confidence_interval = Column(JSON)
    
    # Cache metadata
    hit_count = Column(Integer, default=0)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    model = relationship("PredictionModel")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ModelTrainingJob(Base):
    """Model training job tracking"""
    __tablename__ = "model_training_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("prediction_models.id"), nullable=False)
    
    # Job metadata
    job_name = Column(String(200), nullable=False)
    training_config = Column(JSON)
    
    # Data configuration
    training_data_config = Column(JSON)
    validation_data_config = Column(JSON)
    
    # Training parameters
    hyperparameters = Column(JSON)
    training_algorithm = Column(String(50))
    
    # Status and progress
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    progress_percent = Column(Float, default=0.0)
    current_epoch = Column(Integer, default=0)
    total_epochs = Column(Integer)
    
    # Results
    final_metrics = Column(JSON)
    training_history = Column(JSON)  # Loss curves, metrics over time
    model_artifacts = Column(JSON)  # Paths to saved models, logs, etc.
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)
    
    # Relationships
    model = relationship("PredictionModel")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
