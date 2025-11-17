import joblib
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

from core.config import settings

MODEL_VERSION = "1.0.0"
VECTORIZER_PATH = os.path.join(settings.PATH_MODELS, "nlp_tickets", "vectorizer.pkl")
MODEL_PATH = os.path.join(settings.PATH_MODELS, "nlp_tickets", "model.pkl")
DATA_PATH = os.path.join(settings.PATH_DATA, "raw", "tickets.csv")


_vectorizer = None
_model = None
_df_tickets = None

def load_model():
    """Loads the NLP model and vectorizer from disk."""
    global _vectorizer, _model, _df_tickets

    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(f"Vectorizer not found at {VECTORIZER_PATH}")
    _vectorizer = joblib.load(VECTORIZER_PATH)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    _model = joblib.load(MODEL_PATH)

    # Load historical ticket data for suggestion feature
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Tickets data file not found at {DATA_PATH}")
    _df_tickets = pd.read_csv(DATA_PATH)
    _df_tickets.dropna(subset=['descripcion', 'solucion'], inplace=True)

    return _vectorizer, _model, _df_tickets

def classify_ticket(description: str) -> Dict:
    """
    Classifies a ticket based on its description.
    """
    if _model is None or _vectorizer is None:
        load_model()

    # Vectorize the input description
    description_tfidf = _vectorizer.transform([description])

    # Predict category and confidence score
    predicted_category = _model.predict(description_tfidf)[0]

    # Getting a confidence score for LinearSVC is not straightforward.
    # We can use the decision_function as a proxy for confidence.
    decision_values = _model.decision_function(description_tfidf)[0]
    confidence_score = (1.0 / (1.0 + pow(2, -abs(max(decision_values))))) * 2 - 1  # Simplified sigmoid-like scaling

    return {
        "categoria_predicha": predicted_category,
        "score_confianza": round(float(confidence_score), 4)
    }

def suggest_solutions(description: str, top_n: int = 3) -> List[Dict]:
    """
    Suggests solutions from historical tickets based on text similarity.
    """
    if _df_tickets is None or _vectorizer is None:
        load_model()

    # Vectorize the input description and all historical descriptions
    description_tfidf = _vectorizer.transform([description])
    historical_tfidf = _vectorizer.transform(_df_tickets['descripcion'])

    # Calculate cosine similarity
    similarities = cosine_similarity(description_tfidf, historical_tfidf).flatten()

    # Get the indices of the top N most similar tickets
    top_indices = similarities.argsort()[-top_n:][::-1]

    # Get the suggested solutions
    suggestions = []
    for i in top_indices:
        suggestion = _df_tickets.iloc[i]
        suggestions.append({
            "resumen": suggestion['solucion'][:100] + '...', # Short summary
            "fuente_ticket_id": suggestion['ticket_id'],
            "similarity_score": round(float(similarities[i]), 4)
        })

    return suggestions

# Example usage
if __name__ == '__main__':
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Running training script...")
        from train_nlp import train_nlp_model
        train_nlp_model()

    sample_description = "El motor del coche hace un ruido muy fuerte al arrancar y parece que vibra mucho. Necesito que lo revisen."

    try:
        classification = classify_ticket(sample_description)
        print(f"Classification result: {classification}")

        solutions = suggest_solutions(sample_description)
        print(f"Suggested solutions: {solutions}")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
