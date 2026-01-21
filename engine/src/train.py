"""
Phase 1E: Model Training
Credit Worthiness Assessment - ML Pipeline
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


# Paths
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"


def load_preprocessed_data():
    """Load preprocessed train/test data."""
    X_train = pd.read_csv(MODELS_DIR / "X_train.csv")
    X_test = pd.read_csv(MODELS_DIR / "X_test.csv")
    y_train = pd.read_csv(MODELS_DIR / "y_train.csv").values.ravel()
    y_test = pd.read_csv(MODELS_DIR / "y_test.csv").values.ravel()

    print(f"Train: {X_train.shape} | Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test


def get_models():
    """Define models with class weight handling."""

    # Calculate class weight ratio for XGBoost
    # scale_pos_weight = negative_count / positive_count ≈ 2

    models = {
        'Logistic Regression': LogisticRegression(
            class_weight='balanced',
            max_iter=1000,
            random_state=42
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        ),
        'XGBoost': XGBClassifier(
            n_estimators=100,
            scale_pos_weight=2,
            random_state=42,
            eval_metric='logloss',
            verbosity=0
        ),
        'LightGBM': LGBMClassifier(
            n_estimators=100,
            class_weight='balanced',
            random_state=42,
            verbose=-1
        )
    }

    return models


def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics."""
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_prob)
    }

    return metrics


def train_and_evaluate(models, X_train, X_test, y_train, y_test):
    """Train all models and collect results."""
    results = {}
    trained_models = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")

        # Train
        model.fit(X_train, y_train)
        trained_models[name] = model

        # Cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')

        # Test evaluation
        metrics = evaluate_model(model, X_test, y_test)
        metrics['cv_roc_auc_mean'] = cv_scores.mean()
        metrics['cv_roc_auc_std'] = cv_scores.std()

        results[name] = metrics

        # Print results
        print(f"  CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        print(f"  Test ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"  Test F1: {metrics['f1']:.4f}")

    return results, trained_models


def select_best_model(results, trained_models):
    """Select best model based on ROC-AUC."""
    best_name = max(results, key=lambda x: results[x]['roc_auc'])
    best_model = trained_models[best_name]
    best_score = results[best_name]['roc_auc']

    print(f"\nBest Model: {best_name} (ROC-AUC: {best_score:.4f})")
    return best_name, best_model


def save_results(results, best_name, best_model):
    """Save training results and best model."""
    # Save best model
    joblib.dump(best_model, MODELS_DIR / "model.pkl")

    # Save results
    results_path = MODELS_DIR / "training_results.json"
    with open(results_path, 'w') as f:
        json.dump({
            'best_model': best_name,
            'results': results
        }, f, indent=2)

    print(f"\nSaved:")
    print(f"  - model.pkl (best model: {best_name})")
    print(f"  - training_results.json")


def print_comparison_table(results):
    """Print comparison table of all models."""
    print("\n" + "=" * 70)
    print("MODEL COMPARISON")
    print("=" * 70)
    print(f"{'Model':<22} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10} {'ROC-AUC':>10}")
    print("-" * 70)

    for name, metrics in results.items():
        print(f"{name:<22} {metrics['accuracy']:>10.4f} {metrics['precision']:>10.4f} "
              f"{metrics['recall']:>10.4f} {metrics['f1']:>10.4f} {metrics['roc_auc']:>10.4f}")

    print("=" * 70)


def run_training():
    """Main training pipeline."""
    print("=" * 60)
    print("PHASE 1E: MODEL TRAINING")
    print("=" * 60)

    # Load data
    print("\n[1/4] Loading preprocessed data...")
    X_train, X_test, y_train, y_test = load_preprocessed_data()

    # Get models
    print("\n[2/4] Initializing models...")
    models = get_models()
    print(f"Models: {', '.join(models.keys())}")

    # Train and evaluate
    print("\n[3/4] Training and evaluating models...")
    results, trained_models = train_and_evaluate(models, X_train, X_test, y_train, y_test)

    # Print comparison
    print_comparison_table(results)

    # Select best
    print("\n[4/4] Selecting best model...")
    best_name, best_model = select_best_model(results, trained_models)

    # Save
    save_results(results, best_name, best_model)

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)

    return results, best_model


if __name__ == "__main__":
    results, best_model = run_training()
