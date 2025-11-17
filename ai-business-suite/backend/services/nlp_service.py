from schemas.nlp_tickets import TicketDescriptionRequest
from models_ml.nlp_tickets.predict_nlp import classify_ticket, suggest_solutions, MODEL_VERSION
import logging

logger = logging.getLogger(__name__)

def get_ticket_classification(request: TicketDescriptionRequest) -> dict:
    """
    Processes a ticket classification request.
    """
    try:
        classification_result = classify_ticket(request.descripcion)
        classification_result['model_version'] = MODEL_VERSION
        return classification_result
    except FileNotFoundError:
        logger.error("NLP model or vectorizer not found.")
        raise
    except Exception as e:
        logger.error(f"Error during ticket classification: {e}")
        raise ValueError("Failed to classify ticket.")

def get_ticket_suggestions(request: TicketDescriptionRequest) -> dict:
    """
    Processes a ticket suggestion request.
    """
    try:
        # First, classify the ticket to provide context
        classification_result = classify_ticket(request.descripcion)

        # Then, find similar solutions
        suggested_solutions_list = suggest_solutions(request.descripcion)

        return {
            "categoria_predicha": classification_result['categoria_predicha'],
            "soluciones_sugeridas": suggested_solutions_list,
            "model_version": MODEL_VERSION
        }
    except FileNotFoundError:
        logger.error("NLP model, vectorizer, or data file not found.")
        raise
    except Exception as e:
        logger.error(f"Error during solution suggestion: {e}")
        raise ValueError("Failed to suggest solutions.")
