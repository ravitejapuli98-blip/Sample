"""
Prediction endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.prediction import PredictionModel, Prediction, ModelEvaluation
from app.models.city import City
from app.models.policy import Policy
from app.schemas.prediction import (
    PredictionModelCreate, PredictionModelResponse,
    PredictionCreate, PredictionResponse,
    ModelEvaluationResponse
)

router = APIRouter()


@router.get("/models/", response_model=List[PredictionModelResponse])
async def get_prediction_models(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    model_type: Optional[str] = Query(None),
    target_variable: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of prediction models"""
    query = db.query(PredictionModel)
    
    if model_type:
        query = query.filter(PredictionModel.model_type == model_type)
    if target_variable:
        query = query.filter(PredictionModel.target_variable == target_variable)
    if status:
        query = query.filter(PredictionModel.status == status)
    
    models = query.offset(skip).limit(limit).all()
    return models


@router.get("/models/{model_id}", response_model=PredictionModelResponse)
async def get_prediction_model(model_id: int, db: Session = Depends(get_db)):
    """Get prediction model by ID"""
    model = db.query(PredictionModel).filter(PredictionModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Prediction model not found")
    return model


@router.post("/models/", response_model=PredictionModelResponse)
async def create_prediction_model(model: PredictionModelCreate, db: Session = Depends(get_db)):
    """Create a new prediction model"""
    db_model = PredictionModel(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


@router.get("/models/{model_id}/evaluations", response_model=List[ModelEvaluationResponse])
async def get_model_evaluations(model_id: int, db: Session = Depends(get_db)):
    """Get evaluations for a prediction model"""
    model = db.query(PredictionModel).filter(PredictionModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Prediction model not found")
    
    evaluations = db.query(ModelEvaluation).filter(
        ModelEvaluation.model_id == model_id
    ).order_by(ModelEvaluation.evaluation_date.desc()).all()
    return evaluations


@router.get("/", response_model=List[PredictionResponse])
async def get_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    model_id: Optional[int] = Query(None),
    city_id: Optional[int] = Query(None),
    policy_id: Optional[int] = Query(None),
    prediction_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of predictions"""
    query = db.query(Prediction)
    
    if model_id:
        query = query.filter(Prediction.model_id == model_id)
    if city_id:
        query = query.filter(Prediction.city_id == city_id)
    if policy_id:
        query = query.filter(Prediction.policy_id == policy_id)
    if prediction_type:
        query = query.filter(Prediction.prediction_type == prediction_type)
    
    predictions = query.offset(skip).limit(limit).all()
    return predictions


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Get prediction by ID"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction


@router.post("/", response_model=PredictionResponse)
async def create_prediction(prediction: PredictionCreate, db: Session = Depends(get_db)):
    """Create a new prediction"""
    # Verify model exists
    model = db.query(PredictionModel).filter(PredictionModel.id == prediction.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Prediction model not found")
    
    # Verify city exists
    city = db.query(City).filter(City.id == prediction.city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Verify policy exists if specified
    if prediction.policy_id:
        policy = db.query(Policy).filter(Policy.id == prediction.policy_id).first()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
    
    db_prediction = Prediction(**prediction.dict())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction


@router.post("/predict/{model_id}")
async def make_prediction(
    model_id: int,
    input_data: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Make a prediction using a trained model"""
    model = db.query(PredictionModel).filter(PredictionModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Prediction model not found")
    
    if model.status != "trained":
        raise HTTPException(status_code=400, detail="Model is not trained")
    
    # In a real implementation, this would load the model and make predictions
    # For now, return a mock prediction
    prediction_result = {
        "predicted_value": 42.5,
        "confidence_interval": {"lower": 38.2, "upper": 46.8},
        "prediction_probability": 0.85
    }
    
    return {
        "model_id": model_id,
        "input_data": input_data,
        "prediction": prediction_result,
        "timestamp": datetime.utcnow()
    }
