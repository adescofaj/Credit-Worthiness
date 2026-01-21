"""
Pydantic schemas for Credit Worthiness API
"""

from pydantic import BaseModel, Field
from typing import Optional


# ==================== EXTRACT SCHEMAS ====================

class ExtractResponse(BaseModel):
    """Response from /extract endpoint - extracted financial variables."""

    # Extracted financial variables
    total_monthly_inflow: float = Field(..., description="Total credits/deposits")
    total_monthly_outflow: float = Field(..., description="Total debits/withdrawals")
    transaction_frequency: int = Field(..., description="Number of transactions")
    salary_payment_detected: str = Field(..., description="'Yes' or 'No'")
    end_of_month_balance: float = Field(..., description="Balance at end of month")
    highest_credit_amount: float = Field(..., description="Highest single credit")
    highest_debit_amount: float = Field(..., description="Highest single debit")
    gambling_transactions_count: int = Field(..., description="Count of gambling transactions")
    loan_related_transactions_count: int = Field(..., description="Count of loan transactions")

    # Metadata
    extraction_confidence: str = Field(..., description="'High', 'Medium', or 'Low'")
    source_file_type: str = Field(..., description="'PDF' or 'CSV'")


# ==================== PREDICT SCHEMAS ====================

class PredictRequest(BaseModel):
    """Request for /predict endpoint."""

    # Demographics (from user input)
    age: int = Field(..., ge=18, le=100, description="Age of applicant")
    gender: str = Field(..., description="'Male' or 'Female'")
    employment_status: str = Field(..., description="'Employed', 'Self-employed', or 'Unemployed'")

    # Financial (from /extract or manual input)
    total_monthly_inflow: float = Field(..., ge=0)
    total_monthly_outflow: float = Field(..., ge=0)
    transaction_frequency: int = Field(..., ge=0)
    salary_payment_detected: str = Field(..., description="'Yes' or 'No'")
    end_of_month_balance: float
    highest_credit_amount: float = Field(..., ge=0)
    highest_debit_amount: float = Field(..., ge=0)
    gambling_transactions_count: int = Field(..., ge=0)
    loan_related_transactions_count: int = Field(..., ge=0)

    # Loan History (from user input)
    previous_loan_taken: str = Field(..., description="'Yes' or 'No'")
    previous_loan_amount: float = Field(default=0, ge=0)
    repayment_status: str = Field(default="N/A", description="'On-time', 'Late', or 'N/A'")
    missed_payment_count: int = Field(default=0, ge=0)

    # Behaviour (from user input)
    airtime_spend_per_month: float = Field(..., ge=0)
    data_subscription_spend: float = Field(..., ge=0)


class PredictResponse(BaseModel):
    """Response from /predict endpoint."""

    loan_defaulted: int = Field(..., description="0 or 1")
    default_probability: float = Field(..., ge=0, le=1, description="Probability of default")
    credit_score: int = Field(..., ge=0, le=100, description="Credit score 0-100")
    risk_category: str = Field(..., description="'Low', 'Medium', or 'High'")


# ==================== FEEDBACK SCHEMAS ====================

class FeedbackRequest(BaseModel):
    """Request for /feedback endpoint."""

    # User info
    name: Optional[str] = Field(default="", description="User's name for personalization")
    age: int = Field(..., ge=18, le=100)
    employment_status: str

    # Financial data
    total_monthly_inflow: float
    total_monthly_outflow: float
    end_of_month_balance: float
    salary_payment_detected: str
    transaction_frequency: int
    gambling_transactions_count: int = Field(default=0)

    # Loan history
    previous_loan_taken: str
    repayment_status: str = Field(default="N/A")
    missed_payment_count: int = Field(default=0)

    # Assessment results
    credit_score: int
    risk_category: str
    default_probability: float


class FeedbackResponse(BaseModel):
    """Response from /feedback endpoint."""

    feedback: str = Field(..., description="AI-generated personalized feedback message")
