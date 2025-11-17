from schemas.risk_scoring import RiskScoringRequest
from models_ml.risk_scoring.predict_risk import get_risk_prediction, MODEL_VERSION
import logging

logger = logging.getLogger(__name__)

def get_risk_score(request: RiskScoringRequest) -> dict:
    """
    Processes a risk scoring request and returns the prediction from the model.
    """
    try:
        customer_data = request.dict()

        # The prediction function returns a dict with prob_riesgo, bucket, and explanation
        prediction_result = get_risk_prediction(customer_data)

        # Add the model version to the response
        prediction_result['model_version'] = MODEL_VERSION

        return prediction_result

    except FileNotFoundError:
        logger.error("Risk scoring model not found.")
        raise
    except Exception as e:
        logger.error(f"Error during risk scoring: {e}")
        # Re-raise as a more generic exception to be handled by the router
        raise ValueError("Failed to get risk score.")
