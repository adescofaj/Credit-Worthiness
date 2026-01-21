"""
Phase 1D: Data Preprocessing
Credit Worthiness Assessment - ML Pipeline
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data.csv"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)


def load_data():
    """Load the dataset."""
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df):,} records")
    return df


def create_features(df):
    """Create new engineered features."""
    df = df.copy()

    # Savings rate: how much of income is saved
    df['savings_rate'] = (df['total_monthly_inflow'] - df['total_monthly_outflow']) / df['total_monthly_inflow']
    df['savings_rate'] = df['savings_rate'].clip(-1, 1)  # Cap extreme values

    # Balance ratio: end balance relative to income
    df['balance_ratio'] = df['end_of_month_balance'] / df['total_monthly_inflow']
    df['balance_ratio'] = df['balance_ratio'].clip(0, 5)  # Cap extreme values

    # Debt to income: previous loan relative to annual income
    annual_income = df['total_monthly_inflow'] * 12
    df['debt_to_income'] = df['previous_loan_amount'] / annual_income
    df['debt_to_income'] = df['debt_to_income'].fillna(0).clip(0, 10)

    # Spending ratio: outflow relative to inflow
    df['spending_ratio'] = df['total_monthly_outflow'] / df['total_monthly_inflow']
    df['spending_ratio'] = df['spending_ratio'].clip(0, 2)

    print("Created 4 new features: savings_rate, balance_ratio, debt_to_income, spending_ratio")
    return df


def handle_missing_values(df):
    """Handle missing values in repayment_status."""
    df = df.copy()

    # Fill missing repayment_status with 'No_Loan' (users without previous loans)
    df['repayment_status'] = df['repayment_status'].fillna('No_Loan')

    print(f"Filled {df['repayment_status'].value_counts()['No_Loan']:,} missing repayment_status with 'No_Loan'")
    return df


def encode_features(df):
    """Encode categorical features."""
    df = df.copy()

    # Binary encoding
    df['gender'] = (df['gender'] == 'Male').astype(int)
    df['salary_payment_detected'] = (df['salary_payment_detected'] == 'Yes').astype(int)
    df['previous_loan_taken'] = (df['previous_loan_taken'] == 'Yes').astype(int)

    # One-hot encoding for employment_status
    emp_dummies = pd.get_dummies(df['employment_status'], prefix='emp', drop_first=True)
    df = pd.concat([df, emp_dummies], axis=1)
    df = df.drop('employment_status', axis=1)

    # One-hot encoding for repayment_status
    repay_dummies = pd.get_dummies(df['repayment_status'], prefix='repay', drop_first=True)
    df = pd.concat([df, repay_dummies], axis=1)
    df = df.drop('repayment_status', axis=1)

    # Drop state_of_residence (weak predictor, too many categories)
    df = df.drop('state_of_residence', axis=1)

    print("Encoded categorical features")
    return df


def prepare_data(df):
    """Prepare features and target."""
    # Target
    y = df['loan_defaulted']

    # Features (drop target)
    X = df.drop('loan_defaulted', axis=1)

    print(f"Features: {X.shape[1]}, Target: loan_defaulted")
    return X, y


def scale_features(X_train, X_test):
    """Scale numerical features."""
    # Numerical columns to scale
    numerical_cols = [
        'age', 'total_monthly_inflow', 'total_monthly_outflow',
        'transaction_frequency', 'end_of_month_balance',
        'highest_credit_amount', 'highest_debit_amount',
        'gambling_transactions_count', 'loan_related_transactions_count',
        'previous_loan_amount', 'missed_payment_count',
        'airtime_spend_per_month', 'data_subscription_spend',
        'savings_rate', 'balance_ratio', 'debt_to_income', 'spending_ratio'
    ]

    scaler = StandardScaler()

    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
    X_test_scaled[numerical_cols] = scaler.transform(X_test[numerical_cols])

    print(f"Scaled {len(numerical_cols)} numerical features")
    return X_train_scaled, X_test_scaled, scaler


def save_artifacts(X_train, X_test, y_train, y_test, scaler, feature_names):
    """Save preprocessed data and artifacts."""
    # Save scaler
    joblib.dump(scaler, MODELS_DIR / "scaler.pkl")

    # Save feature names
    feature_info = {
        'feature_names': feature_names,
        'n_features': len(feature_names)
    }
    with open(MODELS_DIR / "features.json", 'w') as f:
        json.dump(feature_info, f, indent=2)

    # Save processed data
    X_train.to_csv(MODELS_DIR / "X_train.csv", index=False)
    X_test.to_csv(MODELS_DIR / "X_test.csv", index=False)
    y_train.to_csv(MODELS_DIR / "y_train.csv", index=False)
    y_test.to_csv(MODELS_DIR / "y_test.csv", index=False)

    print(f"\nArtifacts saved to {MODELS_DIR}/")
    print(f"  - scaler.pkl")
    print(f"  - features.json")
    print(f"  - X_train.csv, X_test.csv, y_train.csv, y_test.csv")


def run_preprocessing():
    """Main preprocessing pipeline."""
    print("=" * 60)
    print("PHASE 1D: DATA PREPROCESSING")
    print("=" * 60)

    # Step 1: Load data
    print("\n[1/7] Loading data...")
    df = load_data()

    # Step 2: Handle missing values
    print("\n[2/7] Handling missing values...")
    df = handle_missing_values(df)

    # Step 3: Feature engineering
    print("\n[3/7] Creating new features...")
    df = create_features(df)

    # Step 4: Encode categoricals
    print("\n[4/7] Encoding categorical features...")
    df = encode_features(df)

    # Step 5: Prepare X and y
    print("\n[5/7] Preparing features and target...")
    X, y = prepare_data(df)

    # Step 6: Train/test split
    print("\n[6/7] Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

    # Step 7: Scale features
    print("\n[7/7] Scaling numerical features...")
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    # Save artifacts
    print("\n" + "-" * 60)
    print("Saving artifacts...")
    save_artifacts(X_train_scaled, X_test_scaled, y_train, y_test, scaler, list(X.columns))

    # Summary
    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETE")
    print("=" * 60)
    print(f"\nDataset shape: {X.shape}")
    print(f"Train set: {X_train_scaled.shape}")
    print(f"Test set: {X_test_scaled.shape}")
    print(f"\nTarget distribution (train):")
    print(f"  No Default: {(y_train == 0).sum():,} ({(y_train == 0).mean()*100:.1f}%)")
    print(f"  Default: {(y_train == 1).sum():,} ({(y_train == 1).mean()*100:.1f}%)")

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler = run_preprocessing()
