import joblib
import os
import pandas as pd
import numpy as np
from typing import List, Dict

from core.config import settings

MODEL_VERSION = "1.0.0"
MODEL_PATH = os.path.join(settings.PATH_MODELS, "forecast", "model.pkl")

_model = None

def load_model():
    """Loads the forecast model from disk."""
    global _model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    _model = joblib.load(MODEL_PATH)
    return _model

def predict_next_month(item_code: str, whs_code: str, history_months: List[Dict[str, any]]) -> float:
    """
    Predicts the sales demand for the next month for a given item and warehouse.

    Args:
        item_code (str): The item's code.
        whs_code (str): The warehouse's code.
        history_months (List[Dict]): A list of dictionaries, each containing 'month' (YYYY-MM) and 'quantity'.

    Returns:
        float: The predicted quantity for the next month.
    """
    if _model is None:
        load_model()

    if not history_months:
        raise ValueError("History months cannot be empty.")

    # Create a DataFrame from the historical data
    df_history = pd.DataFrame(history_months)
    df_history['month'] = pd.to_datetime(df_history['month'], format='%Y-%m')
    df_history.sort_values('month', inplace=True)

    # Determine the next month to predict
    last_month = df_history['month'].max()
    predict_month = last_month + pd.DateOffset(months=1)

    # Create features for the prediction
    features = {}

    # Time-based features
    features['month_num'] = predict_month.month
    features['year'] = predict_month.year
    features['is_end_of_year'] = 1 if predict_month.month in [11, 12] else 0

    # Lag features
    # We need to create a continuous series to correctly get the lags
    required_lags = [1, 2, 3, 6, 12]

    # Create a full date range to handle missing months
    full_date_range = pd.date_range(end=last_month, periods=max(required_lags), freq='MS')

    # Create a series with month as index for easy lookup
    ts = df_history.set_index('month')['quantity']

    # Reindex to ensure all months are present, filling missing with 0
    ts = ts.reindex(full_date_range, fill_value=0)

    for lag in required_lags:
        lag_date = predict_month - pd.DateOffset(months=lag)
        # Find the value for the lag month. If not in history, use 0.
        if lag_date in ts.index:
            features[f'lag_{lag}'] = ts[lag_date]
        else:
            features[f'lag_{lag}'] = 0 # Default to 0 if history is not long enough

    # Create a DataFrame for prediction
    df_predict = pd.DataFrame([features])

    # Ensure column order is the same as in training
    feature_order = [f'lag_{lag}' for lag in [1, 2, 3, 6, 12]] + ['month_num', 'year', 'is_end_of_year']
    df_predict = df_predict[feature_order]

    # Make prediction
    prediction = _model.predict(df_predict)

    return float(prediction[0])

# Example usage (for testing)
if __name__ == '__main__':
    # This requires the model to be trained first
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Running training script...")
        from train_forecast import train_forecast_model
        train_forecast_model()

    # Example historical data
    sample_history = [
        {"month": "2024-10", "quantity": 150},
        {"month": "2024-09", "quantity": 120},
        {"month": "2024-08", "quantity": 110},
        {"month": "2024-07", "quantity": 100},
        {"month": "2024-06", "quantity": 95},
        {"month": "2024-05", "quantity": 90},
        {"month": "2024-04", "quantity": 85},
        {"month": "2024-03", "quantity": 80},
        {"month": "2024-02", "quantity": 75},
        {"month": "2024-01", "quantity": 70},
        {"month": "2023-11", "quantity": 180}, # End of year peak
        {"month": "2023-10", "quantity": 140},
    ]

    try:
        predicted_demand = predict_next_month("ITM001", "WHS01", sample_history)
        print(f"Predicted demand for next month: {predicted_demand:.2f}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
