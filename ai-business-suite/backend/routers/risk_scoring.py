from fastapi import APIRouter, HTTPException

from schemas.risk_scoring import RiskScoringRequest, RiskScoringResponse
from services import risk_service
from models_ml.risk_scoring.predict_risk import load_model

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    """Load the risk model at startup."""
    try:
        load_model()
    except FileNotFoundError:
        raise RuntimeError("Risk scoring model not found. Please train the model first.")

@router.post("/score", response_model=RiskScoringResponse)
def score_customer_risk(request: RiskScoringRequest):
    """
    Calculates the credit risk for a customer based on input features.
    """
    try:
        result = risk_service.get_risk_score(request)
        return RiskScoringResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred during risk scoring.")
