import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import os
import logging

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_risk_model():
    """
    Trains a credit risk scoring model and saves the pipeline.
    """
    logger.info("Starting risk scoring model training...")

    # Load data
    data_path = os.path.join(settings.PATH_DATA, "raw", "riesgo_clientes.csv")
    if not os.path.exists(data_path):
        logger.error(f"Data file not found at {data_path}")
        return

    df = pd.read_csv(data_path)

    # Define features and target
    target = 'target_mora'
    numerical_features = ['amount', 'payment_terms_days', 'past_due_count', 'avg_days_past_due']
    categorical_features = ['segment', 'city']

    # Drop the identifier column as it's not a feature
    if 'customer_id' in df.columns:
        df = df.drop('customer_id', axis=1)

    X = df.drop(target, axis=1)
    y = df[target]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Create preprocessing pipelines for numerical and categorical features
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough' # Keep other columns if any
    )

    # Create the full pipeline with a classifier
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(random_state=42, class_weight='balanced'))
    ])

    # Train model
    logger.info("Training LogisticRegression model...")
    model.fit(X_train, y_train)

    # Evaluate model
    logger.info("Evaluating model...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    logger.info(f"Model Evaluation:\n"
                f"Accuracy: {accuracy:.4f}\n"
                f"Precision: {precision:.4f}\n"
                f"Recall: {recall:.4f}\n"
                f"F1-Score: {f1:.4f}\n"
                f"ROC-AUC: {roc_auc:.4f}")

    # Save the entire pipeline
    model_dir = os.path.join(settings.PATH_MODELS, "risk_scoring")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model, model_path)
    logger.info(f"Model pipeline saved to {model_path}")

if __name__ == "__main__":
    train_risk_model()
