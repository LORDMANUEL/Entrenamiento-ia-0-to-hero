from fastapi import APIRouter, HTTPException
from typing import List

from schemas.forecast import (
    ForecastPredictionRequest,
    ForecastPredictionResponse,
    TopItemsResponse,
    TopItem
)
from services import forecast_service
from models_ml.forecast.predict_forecast import load_model

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    """Load the model at startup."""
    try:
        load_model()
    except FileNotFoundError:
        raise RuntimeError("Forecast model not found. Please train the model first by running the training script.")

@router.post("/predict", response_model=ForecastPredictionResponse)
def predict_demand(request: ForecastPredictionRequest):
    """
    Predicts sales demand for the next month based on historical data.
    """
    if not request.history_months:
        raise HTTPException(status_code=400, detail="History months cannot be empty.")

    try:
        result = forecast_service.get_forecast_prediction(request)
        return ForecastPredictionResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred during prediction.")

@router.get("/top-items", response_model=TopItemsResponse)
def get_top_items():
    """
    Gets a list of items with the highest predicted demand for the next month.
    """
    try:
        top_items = forecast_service.get_top_items_forecast()
        if not top_items:
            # This could be a 204 No Content, but 200 with empty list is often simpler for clients
            return TopItemsResponse(top_items=[])
        return TopItemsResponse(top_items=top_items)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to calculate top items forecast.")
