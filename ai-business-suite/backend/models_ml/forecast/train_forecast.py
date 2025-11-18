import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os
import logging

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_forecast_model():
    """
    Trains a sales forecast model and saves it.
    """
    logger.info("Starting forecast model training...")

    # Load data
    data_path = os.path.join(settings.PATH_DATA, "raw", "ventas_repuestos.csv")
    if not os.path.exists(data_path):
        logger.error(f"Data file not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    df['doc_date'] = pd.to_datetime(df['doc_date'])

    # Feature Engineering
    logger.info("Performing feature engineering...")
    df.set_index('doc_date', inplace=True)

    # Resample to monthly sales per item and warehouse
    monthly_sales = df.groupby(['item_code', 'whs_code', pd.Grouper(freq='M')])['quantity'].sum().reset_index()
    monthly_sales = monthly_sales.rename(columns={'doc_date': 'month'})
    monthly_sales.sort_values(by=['item_code', 'whs_code', 'month'], inplace=True)

    # Create lag features
    for lag in [1, 2, 3, 6, 12]:
        monthly_sales[f'lag_{lag}'] = monthly_sales.groupby(['item_code', 'whs_code'])['quantity'].shift(lag)

    # Create time-based features
    monthly_sales['month_num'] = monthly_sales['month'].dt.month
    monthly_sales['year'] = monthly_sales['month'].dt.year
    monthly_sales['is_end_of_year'] = monthly_sales['month_num'].isin([11, 12]).astype(int)

    # Drop rows with NaN values created by lag features
    monthly_sales.dropna(inplace=True)

    if monthly_sales.empty:
        logger.error("No data available for training after feature engineering.")
        return

    # Define features and target
    features = [f'lag_{lag}' for lag in [1, 2, 3, 6, 12]] + ['month_num', 'year', 'is_end_of_year']
    target = 'quantity'

    X = monthly_sales[features]
    y = monthly_sales[target]

    # Split data (time-series aware)
    # A simple split for this example. For a real case, TimeSeriesSplit is better.
    split_date = monthly_sales['month'].max() - pd.DateOffset(months=6)
    train_df = monthly_sales[monthly_sales['month'] <= split_date]
    test_df = monthly_sales[monthly_sales['month'] > split_date]

    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]

    if X_train.empty or X_test.empty:
        logger.error("Not enough data to perform train-test split.")
        return

    logger.info(f"Training data shape: {X_train.shape}")
    logger.info(f"Testing data shape: {X_test.shape}")

    # Train model
    logger.info("Training RandomForestRegressor model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=5, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate model
    logger.info("Evaluating model...")
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    # Calculate MAPE carefully to avoid division by zero
    mape = np.mean(np.abs((y_test - predictions) / np.where(y_test == 0, 1, y_test))) * 100

    logger.info(f"Model Evaluation:\nMAE: {mae:.2f}\nRMSE: {rmse:.2f}\nMAPE: {mape:.2f}%")

    # Save model
    model_dir = os.path.join(settings.PATH_MODELS, "forecast")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_forecast_model()
