"""
Preprocessing utilities for inference
Must match Phase 1D preprocessing exactly
"""

import pandas as pd
import numpy as np

# Numerical columns that need scaling (must match Phase 1D)
NUMERICAL_COLS = [
    'age', 'total_monthly_inflow', 'total_monthly_outflow',
    'transaction_frequency', 'end_of_month_balance',
    'highest_credit_amount', 'highest_debit_amount',
    'gambling_transactions_count', 'loan_related_transactions_count',
    'previous_loan_amount', 'missed_payment_count',
    'airtime_spend_per_month', 'data_subscription_spend',
    'savings_rate', 'balance_ratio', 'debt_to_income', 'spending_ratio'
]

# Feature order (must match training)
FEATURE_ORDER = [
    'age', 'gender', 'total_monthly_inflow', 'total_monthly_outflow',
    'transaction_frequency', 'salary_payment_detected', 'end_of_month_balance',
    'highest_credit_amount', 'highest_debit_amount',
    'gambling_transactions_count', 'loan_related_transactions_count',
    'previous_loan_taken', 'previous_loan_amount', 'missed_payment_count',
    'airtime_spend_per_month', 'data_subscription_spend',
    'savings_rate', 'balance_ratio', 'debt_to_income', 'spending_ratio',
    'emp_Self-employed', 'emp_Unemployed', 'repay_No_Loan', 'repay_On-time'
]


def preprocess_input(data: dict, scaler) -> pd.DataFrame:
    """
    Preprocess input data for model prediction.
    Matches Phase 1D preprocessing pipeline exactly.
    """
    df = pd.DataFrame([data])

    # Create engineered features
    df['savings_rate'] = (df['total_monthly_inflow'] - df['total_monthly_outflow']) / df['total_monthly_inflow']
    df['savings_rate'] = df['savings_rate'].clip(-1, 1)

    df['balance_ratio'] = df['end_of_month_balance'] / df['total_monthly_inflow']
    df['balance_ratio'] = df['balance_ratio'].clip(0, 5)

    annual_income = df['total_monthly_inflow'] * 12
    df['debt_to_income'] = df['previous_loan_amount'] / annual_income
    df['debt_to_income'] = df['debt_to_income'].fillna(0).clip(0, 10)

    df['spending_ratio'] = df['total_monthly_outflow'] / df['total_monthly_inflow']
    df['spending_ratio'] = df['spending_ratio'].clip(0, 2)

    # Binary encoding
    df['gender'] = (df['gender'] == 'Male').astype(int)
    df['salary_payment_detected'] = (df['salary_payment_detected'] == 'Yes').astype(int)
    df['previous_loan_taken'] = (df['previous_loan_taken'] == 'Yes').astype(int)

    # One-hot encoding for employment_status
    df['emp_Self-employed'] = (df['employment_status'] == 'Self-employed').astype(int)
    df['emp_Unemployed'] = (df['employment_status'] == 'Unemployed').astype(int)

    # One-hot encoding for repayment_status
    # Handle missing/N/A repayment_status as No_Loan
    repay_status = df['repayment_status'].iloc[0]
    if pd.isna(repay_status) or repay_status == 'N/A':
        repay_status = 'No_Loan'

    df['repay_No_Loan'] = int(repay_status == 'No_Loan')
    df['repay_On-time'] = int(repay_status == 'On-time')

    # Drop original categorical columns
    df = df.drop(['employment_status', 'repayment_status'], axis=1)

    # Scale numerical features
    df[NUMERICAL_COLS] = scaler.transform(df[NUMERICAL_COLS])

    # Ensure correct feature order
    df = df[FEATURE_ORDER]

    return df
