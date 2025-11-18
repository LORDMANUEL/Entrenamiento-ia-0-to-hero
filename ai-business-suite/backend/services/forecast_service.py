import pandas as pd
import os
from typing import List
import logging

from models_ml.forecast.predict_forecast import predict_next_month, MODEL_VERSION
from core.config import settings
from schemas.forecast import ForecastPredictionRequest, TopItem

logger = logging.getLogger(__name__)

def get_forecast_prediction(request: ForecastPredictionRequest) -> dict:
    """
    Gets a forecast prediction for a single item.
    """
    try:
        # Pydantic models automatically convert the list of dicts
        history_dicts = [h.dict() for h in request.history_months]

        predicted_quantity = predict_next_month(
            item_code=request.item_code,
            whs_code=request.whs_code,
            history_months=history_dicts
        )

        return {
            "predicted_quantity": round(predicted_quantity, 2),
            "model_version": MODEL_VERSION
        }
    except FileNotFoundError:
        logger.error("Forecast model not found.")
        raise
    except Exception as e:
        logger.error(f"Error during forecast prediction: {e}")
        raise ValueError("Failed to get forecast prediction.")


def get_top_items_forecast() -> List[TopItem]:
    """
    Generates a forecast for the next month for all items and returns the top N.
    This is an example implementation using historical data as a proxy.
    """
    try:
        # Load historical data to simulate this process
        data_path = os.path.join(settings.PATH_DATA, "raw", "ventas_repuestos.csv")
        if not os.path.exists(data_path):
            logger.error("Sales data file not found for top items forecast.")
            return []

        df = pd.read_csv(data_path)
        df['doc_date'] = pd.to_datetime(df['doc_date'])

        # Get the unique item/warehouse combinations
        unique_items = df[['item_code', 'item_name', 'whs_code']].drop_duplicates().to_dict('records')

        results = []

        # For each item, get its history and predict next month
        for item in unique_items:
            item_history = df[
                (df['item_code'] == item['item_code']) &
                (df['whs_code'] == item['whs_code'])
            ]

            # Resample to monthly sales
            monthly_history = item_history.set_index('doc_date')['quantity'].resample('MS').sum()

            # Ensure we have enough history for the model's features (at least 12 months)
            if len(monthly_history) < 12:
                continue

            # Format for prediction function
            history_for_pred = [
                {"month": idx.strftime('%Y-%m'), "quantity": val}
                for idx, val in monthly_history.items() if val > 0
            ]

            # Predict
            try:
                predicted_quantity = predict_next_month(
                    item_code=item['item_code'],
                    whs_code=item['whs_code'],
                    history_months=history_for_pred
                )

                results.append(TopItem(
                    item_code=item['item_code'],
                    item_name=item['item_name'],
                    whs_code=item['whs_code'],
                    predicted_quantity=round(predicted_quantity, 2)
                ))
            except Exception as e:
                logger.warning(f"Could not generate forecast for {item['item_code']}: {e}")
                continue

        # Sort by predicted quantity and return top 10
        top_items = sorted(results, key=lambda x: x.predicted_quantity, reverse=True)[:10]
        return top_items

    except Exception as e:
        logger.error(f"Error calculating top items forecast: {e}")
        return []
