"""
Model loading and prediction logic
"""

import joblib
from pathlib import Path

from utils.preprocessing import preprocess_input

# Paths to model artifacts
ENGINE_DIR = Path(__file__).parent.parent.parent / "engine" / "models"

# Load model and scaler at startup
model = joblib.load(ENGINE_DIR / "model.pkl")
scaler = joblib.load(ENGINE_DIR / "scaler.pkl")


def predict(data: dict) -> dict:
    """
    Make credit prediction.

    Args:
        data: Dictionary with all input features

    Returns:
        Dictionary with prediction results
    """
    # Preprocess input
    X = preprocess_input(data, scaler)

    # Get prediction and probability
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]  # Probability of default (class 1)

    # Calculate credit score (0-100)
    credit_score = int((1 - probability) * 100)

    # Determine risk category
    if credit_score >= 70:
        risk_category = "Low"
    elif credit_score >= 40:
        risk_category = "Medium"
    else:
        risk_category = "High"

    return {
        "loan_defaulted": int(prediction),
        "default_probability": round(probability, 4),
        "credit_score": credit_score,
        "risk_category": risk_category
    }
