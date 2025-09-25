"""
Pydantic schemas for prediction data
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PredictionModelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    model_type: str = Field(..., min_length=1, max_length=50)
    target_variable: str = Field(..., min_length=1, max_length=100)
    algorithm: str = Field(..., min_length=1, max_length=50)
    model_config: Optional[Dict[str, Any]] = None
    feature_columns: Optional[List[str]] = None
    version: str = Field(default="1.0.0", max_length=20)


class PredictionModelCreate(PredictionModelBase):
    pass


class PredictionModelResponse(PredictionModelBase):
    id: int
    accuracy_score: Optional[float] = None
    r2_score: Optional[float] = None
    mae: Optional[float] = None
    rmse: Optional[float] = None
    model_path: Optional[str] = None
    scaler_path: Optional[str] = None
    feature_importance: Optional[Dict[str, float]] = None
    training_data_size: Optional[int] = None
    training_date_range: Optional[Dict[str, datetime]] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PredictionBase(BaseModel):
    prediction_type: str = Field(..., min_length=1, max_length=50)
    time_horizon: Optional[int] = Field(None, ge=1)
    input_features: Optional[Dict[str, Any]] = None
    prediction_context: Optional[Dict[str, Any]] = None
    scenario_parameters: Optional[Dict[str, Any]] = None


class PredictionCreate(PredictionBase):
    model_id: int = Field(..., ge=1)
    city_id: int = Field(..., ge=1)
    policy_id: Optional[int] = Field(None, ge=1)


class PredictionResponse(PredictionBase):
    id: int
    model_id: int
    city_id: int
    policy_id: Optional[int]
    input_data_hash: Optional[str] = None
    predicted_value: Optional[float] = None
    confidence_interval: Optional[Dict[str, float]] = None
    prediction_probability: Optional[float] = None
    actual_value: Optional[float] = None
    prediction_error: Optional[float] = None
    is_validated: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ModelEvaluationBase(BaseModel):
    evaluation_type: str = Field(..., min_length=1, max_length=50)
    test_data_size: Optional[int] = Field(None, ge=0)
    test_data_date_range: Optional[Dict[str, datetime]] = None


class ModelEvaluationResponse(ModelEvaluationBase):
    id: int
    model_id: int
    evaluation_date: datetime
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    r2_score: Optional[float] = None
    mae: Optional[float] = None
    rmse: Optional[float] = None
    mape: Optional[float] = None
    confusion_matrix: Optional[Dict[str, Any]] = None
    roc_auc: Optional[float] = None
    feature_importance: Optional[Dict[str, float]] = None
    cross_validation_scores: Optional[List[float]] = None
    validation_plots: Optional[Dict[str, str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
