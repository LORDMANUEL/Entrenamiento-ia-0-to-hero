import joblib
import os
import pandas as pd
from typing import Dict, Any

from core.config import settings

MODEL_VERSION = "1.0.0"
MODEL_PATH = os.path.join(settings.PATH_MODELS, "risk_scoring", "model.pkl")

_model_pipeline = None

def load_model():
    """Loads the risk scoring model pipeline from disk."""
    global _model_pipeline
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    _model_pipeline = joblib.load(MODEL_PATH)
    return _model_pipeline

def get_risk_prediction(customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predicts the credit risk for a given set of customer data.

    Args:
        customer_data (Dict[str, Any]): A dictionary with the customer's features.

    Returns:
        Dict[str, Any]: A dictionary containing probability, risk bucket, and explanation.
    """
    if _model_pipeline is None:
        load_model()

    # Convert input dict to a DataFrame, as the pipeline expects it
    df = pd.DataFrame([customer_data])

    # Predict probability of the positive class (target_mora = 1)
    probability = _model_pipeline.predict_proba(df)[:, 1][0]

    # Determine risk bucket and explanation
    if probability < 0.3:
        bucket = "BAJO"
        explanation = "Perfil de bajo riesgo, historial y operación favorables."
    elif probability < 0.6:
        bucket = "MEDIO"
        explanation = "Riesgo moderado. Factores como el monto o historial de pagos requieren atención."
    else:
        bucket = "ALTO"
        explanation = "Alto riesgo detectado. Combinación de alto monto, plazos extendidos o historial de atrasos."

    # Custom explanation based on input data
    if customer_data.get('amount', 0) > 15000:
        explanation += " El monto de la operación es elevado."
    if customer_data.get('past_due_count', 0) > 5:
        explanation += " El cliente presenta un historial de atrasos previos."

    return {
        "prob_riesgo": float(probability),
        "bucket": bucket,
        "explanation": explanation.strip()
    }

# Example usage
if __name__ == '__main__':
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Running training script...")
        from train_risk import train_risk_model
        train_risk_model()

    sample_customer = {
        'customer_id': 'CUST-TEST',
        'segment': 'Empresa',
        'city': 'Madrid',
        'amount': 12000.0,
        'payment_terms_days': 60,
        'past_due_count': 6,
        'avg_days_past_due': 15.5
    }

    try:
        prediction = get_risk_prediction(sample_customer)
        print(f"Risk Prediction: {prediction}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
