"""
Phase 1F: Model Evaluation
Credit Worthiness Assessment - ML Pipeline
"""

import pandas as pd
import numpy as np
import joblib
import json
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import (
    confusion_matrix, classification_report,
    roc_curve, auc, precision_recall_curve,
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)


# Paths
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
PLOTS_DIR = OUTPUTS_DIR / "plots"
REPORTS_DIR = OUTPUTS_DIR / "reports"

# Create directories
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Colors (matching frontend)
COLORS = {
    'primary': '#4B2E05',
    'secondary': '#7B4B2A',
    'accent': '#D4A373',
    'light': '#CBB193',
    'bg': '#F5EDE0',
    'text': '#3C2A21'
}


def load_model_and_data():
    """Load the best model and train/test data."""
    model = joblib.load(MODELS_DIR / "model.pkl")
    X_train = pd.read_csv(MODELS_DIR / "X_train.csv")
    X_test = pd.read_csv(MODELS_DIR / "X_test.csv")
    y_train = pd.read_csv(MODELS_DIR / "y_train.csv").values.ravel()
    y_test = pd.read_csv(MODELS_DIR / "y_test.csv").values.ravel()

    # Load training results
    with open(MODELS_DIR / "training_results.json", 'r') as f:
        training_results = json.load(f)

    print(f"Loaded model: {training_results['best_model']}")
    print(f"Train set: {X_train.shape} | Test set: {X_test.shape}")

    return model, X_train, X_test, y_train, y_test, training_results


def plot_confusion_matrix(y_test, y_pred):
    """Plot confusion matrix."""
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    # Plot heatmap
    im = ax.imshow(cm, cmap='YlOrBr')

    # Labels
    labels = ['No Default', 'Default']
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_yticklabels(labels, fontsize=12)
    ax.set_xlabel('Predicted', fontsize=12, color=COLORS['text'])
    ax.set_ylabel('Actual', fontsize=12, color=COLORS['text'])
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold', color=COLORS['text'])

    # Add text annotations
    for i in range(2):
        for j in range(2):
            color = 'white' if cm[i, j] > cm.max() / 2 else COLORS['text']
            ax.text(j, i, f'{cm[i, j]:,}', ha='center', va='center',
                    fontsize=16, fontweight='bold', color=color)

    plt.colorbar(im)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "confusion_matrix.png", dpi=150, facecolor=COLORS['bg'])
    plt.close()

    print("Saved: confusion_matrix.png")
    return cm


def plot_roc_curve(y_test, y_prob):
    """Plot ROC curve."""
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    # ROC curve
    ax.plot(fpr, tpr, color=COLORS['primary'], lw=2,
            label=f'ROC Curve (AUC = {roc_auc:.4f})')
    ax.fill_between(fpr, tpr, alpha=0.3, color=COLORS['accent'])

    # Diagonal line
    ax.plot([0, 1], [0, 1], color=COLORS['light'], lw=2, linestyle='--', label='Random')

    ax.set_xlabel('False Positive Rate', fontsize=12, color=COLORS['text'])
    ax.set_ylabel('True Positive Rate', fontsize=12, color=COLORS['text'])
    ax.set_title('ROC Curve', fontsize=14, fontweight='bold', color=COLORS['text'])
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "roc_curve.png", dpi=150, facecolor=COLORS['bg'])
    plt.close()

    print("Saved: roc_curve.png")
    return roc_auc


def plot_precision_recall_curve(y_test, y_prob):
    """Plot Precision-Recall curve."""
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    pr_auc = auc(recall, precision)

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    ax.plot(recall, precision, color=COLORS['primary'], lw=2,
            label=f'PR Curve (AUC = {pr_auc:.4f})')
    ax.fill_between(recall, precision, alpha=0.3, color=COLORS['accent'])

    ax.set_xlabel('Recall', fontsize=12, color=COLORS['text'])
    ax.set_ylabel('Precision', fontsize=12, color=COLORS['text'])
    ax.set_title('Precision-Recall Curve', fontsize=14, fontweight='bold', color=COLORS['text'])
    ax.legend(loc='lower left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "precision_recall_curve.png", dpi=150, facecolor=COLORS['bg'])
    plt.close()

    print("Saved: precision_recall_curve.png")
    return pr_auc


def plot_feature_importance(model, feature_names):
    """Plot feature importance."""
    # Get coefficients (for Logistic Regression)
    if hasattr(model, 'coef_'):
        importance = np.abs(model.coef_[0])
    elif hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
    else:
        print("Model doesn't have feature importance")
        return None

    # Sort by importance
    indices = np.argsort(importance)[::-1][:15]  # Top 15
    top_features = [feature_names[i] for i in indices]
    top_importance = importance[indices]

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    colors = [COLORS['primary'] if i % 2 == 0 else COLORS['accent'] for i in range(len(top_features))]
    bars = ax.barh(range(len(top_features)), top_importance[::-1], color=colors[::-1])

    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features[::-1], fontsize=10)
    ax.set_xlabel('Importance (Absolute Coefficient)', fontsize=12, color=COLORS['text'])
    ax.set_title('Top 15 Feature Importance', fontsize=14, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "feature_importance.png", dpi=150, facecolor=COLORS['bg'])
    plt.close()

    print("Saved: feature_importance.png")
    return dict(zip(top_features, top_importance))


def plot_model_comparison(training_results):
    """Plot model comparison bar chart."""
    results = training_results['results']
    models = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    x = np.arange(len(models))
    width = 0.15
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['light'], COLORS['text']]

    for i, metric in enumerate(metrics):
        values = [results[m][metric] for m in models]
        ax.bar(x + i * width, values, width, label=metric.upper(), color=colors[i])

    ax.set_ylabel('Score', fontsize=12, color=COLORS['text'])
    ax.set_title('Model Comparison', fontsize=14, fontweight='bold', color=COLORS['text'])
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(models, rotation=15, ha='right')
    ax.legend(loc='lower right')
    ax.set_ylim(0.6, 1.0)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "model_comparison.png", dpi=150, facecolor=COLORS['bg'])
    plt.close()

    print("Saved: model_comparison.png")


def generate_report(y_test, y_pred, y_prob, training_results, feature_importance, train_metrics=None):
    """Generate evaluation report."""
    report = {
        'best_model': training_results['best_model'],
        'test_metrics': {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_prob)
        },
        'train_metrics': train_metrics,
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'classification_report': classification_report(y_test, y_pred, output_dict=True),
        'top_features': feature_importance,
        'all_models': training_results['results']
    }

    with open(REPORTS_DIR / "evaluation_report.json", 'w') as f:
        json.dump(report, f, indent=2)

    print("Saved: evaluation_report.json")
    return report


def print_train_vs_test(model, X_train, X_test, y_train, y_test):
    """Print train vs test comparison to check for overfitting."""
    # Train predictions
    y_train_pred = model.predict(X_train)
    y_train_prob = model.predict_proba(X_train)[:, 1]

    # Test predictions
    y_test_pred = model.predict(X_test)
    y_test_prob = model.predict_proba(X_test)[:, 1]

    print("\n" + "=" * 60)
    print("TRAIN vs TEST COMPARISON (Overfitting Check)")
    print("=" * 60)
    print(f"{'Metric':<12} {'Train':>12} {'Test':>12} {'Diff':>12}")
    print("-" * 60)

    metrics = [
        ('Accuracy', accuracy_score(y_train, y_train_pred), accuracy_score(y_test, y_test_pred)),
        ('Precision', precision_score(y_train, y_train_pred), precision_score(y_test, y_test_pred)),
        ('Recall', recall_score(y_train, y_train_pred), recall_score(y_test, y_test_pred)),
        ('F1', f1_score(y_train, y_train_pred), f1_score(y_test, y_test_pred)),
        ('ROC-AUC', roc_auc_score(y_train, y_train_prob), roc_auc_score(y_test, y_test_prob)),
    ]

    train_metrics = {}
    for name, train, test in metrics:
        diff = train - test
        print(f'{name:<12} {train:>12.4f} {test:>12.4f} {diff:>+12.4f}')
        train_metrics[name.lower()] = train

    print("-" * 60)
    # Verdict
    avg_diff = np.mean([m[1] - m[2] for m in metrics])
    if avg_diff < 0.05:
        print("Verdict: No overfitting detected (Train ~ Test)")
    else:
        print("Verdict: Possible overfitting (Train >> Test)")
    print("=" * 60)

    return train_metrics


def print_summary(y_test, y_pred, y_prob, training_results):
    """Print evaluation summary."""
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    print("\n" + "=" * 60)
    print("TEST SET EVALUATION SUMMARY")
    print("=" * 60)
    print(f"\nBest Model: {training_results['best_model']}")
    print(f"\nConfusion Matrix:")
    print(f"  True Negatives:  {tn:,}")
    print(f"  False Positives: {fp:,}")
    print(f"  False Negatives: {fn:,}")
    print(f"  True Positives:  {tp:,}")
    print(f"\nTest Metrics:")
    print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"  F1 Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"  ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}")
    print("=" * 60)


def run_evaluation():
    """Main evaluation pipeline."""
    print("=" * 60)
    print("PHASE 1F: MODEL EVALUATION")
    print("=" * 60)

    # Load model and data
    print("\n[1/7] Loading model and data...")
    model, X_train, X_test, y_train, y_test, training_results = load_model_and_data()

    # Get predictions
    print("\n[2/7] Generating predictions...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Plot confusion matrix
    print("\n[3/7] Plotting confusion matrix...")
    cm = plot_confusion_matrix(y_test, y_pred)

    # Plot ROC curve
    print("\n[4/7] Plotting ROC curve...")
    roc_auc = plot_roc_curve(y_test, y_prob)

    # Plot Precision-Recall curve
    print("\n[5/7] Plotting Precision-Recall curve...")
    pr_auc = plot_precision_recall_curve(y_test, y_prob)

    # Plot feature importance
    print("\n[6/7] Plotting feature importance...")
    feature_names = X_test.columns.tolist()
    feature_importance = plot_feature_importance(model, feature_names)

    # Plot model comparison
    print("\n[7/7] Plotting model comparison...")
    plot_model_comparison(training_results)

    # Print train vs test comparison
    train_metrics = print_train_vs_test(model, X_train, X_test, y_train, y_test)

    # Generate report (now includes train_metrics)
    print("\nGenerating evaluation report...")
    report = generate_report(y_test, y_pred, y_prob, training_results, feature_importance, train_metrics)

    # Print test summary
    print_summary(y_test, y_pred, y_prob, training_results)

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)
    print(f"\nPlots saved to: {PLOTS_DIR}")
    print(f"Report saved to: {REPORTS_DIR}")

    return report


if __name__ == "__main__":
    report = run_evaluation()
