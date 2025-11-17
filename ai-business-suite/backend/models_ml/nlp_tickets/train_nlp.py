import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import os
import logging
import seaborn as sns
import matplotlib.pyplot as plt

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_nlp_model():
    """
    Trains a ticket classification model and saves the vectorizer and the model.
    """
    logger.info("Starting NLP ticket classification model training...")

    # Load data
    data_path = os.path.join(settings.PATH_DATA, "raw", "tickets.csv")
    if not os.path.exists(data_path):
        logger.error(f"Data file not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    df.dropna(subset=['descripcion', 'categoria'], inplace=True) # Ensure no missing values in critical columns

    # Define features and target
    X = df['descripcion']
    y = df['categoria']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Vectorizer
    logger.info("Vectorizing text data using TfidfVectorizer...")
    vectorizer = TfidfVectorizer(stop_words=None, max_df=0.8, min_df=3, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train model
    logger.info("Training LinearSVC model...")
    model = LinearSVC(random_state=42, class_weight='balanced', C=0.5)
    model.fit(X_train_tfidf, y_train)

    # Evaluate model
    logger.info("Evaluating model...")
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model Accuracy: {accuracy:.4f}")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    logger.info(f"Confusion Matrix:\n{cm}")

    # Save the vectorizer and the model
    model_dir = os.path.join(settings.PATH_MODELS, "nlp_tickets")
    os.makedirs(model_dir, exist_ok=True)

    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")
    joblib.dump(vectorizer, vectorizer_path)
    logger.info(f"Vectorizer saved to {vectorizer_path}")

    model_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")

    # Optional: Save confusion matrix plot for analysis
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=model.classes_, yticklabels=model.classes_, cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plot_path = os.path.join(model_dir, "confusion_matrix.png")
    plt.savefig(plot_path)
    logger.info(f"Confusion matrix plot saved to {plot_path}")


if __name__ == "__main__":
    train_nlp_model()
