from fastapi import APIRouter, HTTPException

from schemas.nlp_tickets import (
    TicketDescriptionRequest,
    TicketClassificationResponse,
    TicketSuggestionResponse
)
from services import nlp_service
from models_ml.nlp_tickets.predict_nlp import load_model

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    """Load the NLP model and assets at startup."""
    try:
        load_model()
    except FileNotFoundError:
        raise RuntimeError("NLP model assets not found. Please train the model first.")

@router.post("/classify", response_model=TicketClassificationResponse)
def classify_ticket_endpoint(request: TicketDescriptionRequest):
    """
    Classifies a support ticket into a category based on its description.
    """
    try:
        result = nlp_service.get_ticket_classification(request)
        return TicketClassificationResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred during ticket classification.")

@router.post("/suggest", response_model=TicketSuggestionResponse)
def suggest_solutions_endpoint(request: TicketDescriptionRequest):
    """
    Suggests solutions for a support ticket based on historical data.
    """
    try:
        result = nlp_service.get_ticket_suggestions(request)
        return TicketSuggestionResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred during solution suggestion.")
