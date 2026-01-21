"""
AI-powered feedback generation service for credit assessment results.
Uses OpenAI to generate personalized feedback based on user data and model output.
"""

import os
import json
from openai import OpenAI

# Lazy initialization of OpenAI client
_client = None


def get_openai_client():
    """Get or create OpenAI client with lazy initialization."""
    global _client
    if _client is None:
        import httpx
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        # Create custom httpx client without proxy to avoid compatibility issues
        http_client = httpx.Client()
        _client = OpenAI(api_key=api_key, http_client=http_client)
    return _client


FEEDBACK_PROMPT = """You are a credit analyst providing assessment feedback to a financial institution admin reviewing a loan application.

Based on the applicant's financial data and assessment results, generate a professional summary for the reviewing officer.

APPLICANT DATA:
- Name: {name}
- Age: {age}
- Employment Status: {employment_status}
- Monthly Income: ₦{total_monthly_inflow:,.0f}
- Monthly Expenses: ₦{total_monthly_outflow:,.0f}
- End of Month Balance: ₦{end_of_month_balance:,.0f}
- Salary Detected: {salary_payment_detected}
- Transaction Frequency: {transaction_frequency} transactions
- Gambling Transactions: {gambling_transactions_count}
- Previous Loan: {previous_loan_taken}
- Repayment Status: {repayment_status}
- Missed Payments: {missed_payment_count}

ASSESSMENT RESULTS:
- Credit Score: {credit_score}/100
- Risk Category: {risk_category}
- Default Probability: {default_probability:.1%}

INSTRUCTIONS:
1. Write in THIRD PERSON about the applicant (e.g., "This applicant demonstrates..." or "John shows...")
2. Use the applicant's name if provided, otherwise use "This applicant"
3. State the credit standing assessment clearly
4. Highlight 2-3 KEY FACTORS that influenced the score (both positive and concerns)
5. End with a recommendation for the reviewing officer
6. Keep the tone professional and objective
7. Keep the message concise (3-4 sentences max)
8. Do NOT mention specific numbers like "95/100" - use qualitative descriptions instead

For LOW risk: Recommend approval, highlight strengths
For MEDIUM risk: Recommend conditional approval or further review, note strengths and concerns
For HIGH risk: Recommend caution or denial, explain key risk factors

Return ONLY the feedback message, no additional formatting or labels."""


def generate_feedback(user_data: dict, results: dict) -> str:
    """
    Generate personalized feedback using OpenAI.

    Args:
        user_data: Dictionary containing user's financial and demographic data
        results: Dictionary containing model prediction results

    Returns:
        Personalized feedback string
    """
    client = get_openai_client()

    # Merge data for prompt formatting
    prompt_data = {
        "name": user_data.get("name", ""),
        "age": user_data.get("age", 0),
        "employment_status": user_data.get("employment_status", "Unknown"),
        "total_monthly_inflow": user_data.get("total_monthly_inflow", 0),
        "total_monthly_outflow": user_data.get("total_monthly_outflow", 0),
        "end_of_month_balance": user_data.get("end_of_month_balance", 0),
        "salary_payment_detected": user_data.get("salary_payment_detected", "No"),
        "transaction_frequency": user_data.get("transaction_frequency", 0),
        "gambling_transactions_count": user_data.get("gambling_transactions_count", 0),
        "previous_loan_taken": user_data.get("previous_loan_taken", "No"),
        "repayment_status": user_data.get("repayment_status", "N/A"),
        "missed_payment_count": user_data.get("missed_payment_count", 0),
        "credit_score": results.get("credit_score", 0),
        "risk_category": results.get("risk_category", "Unknown"),
        "default_probability": results.get("default_probability", 0),
    }

    formatted_prompt = FEEDBACK_PROMPT.format(**prompt_data)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional credit advisor. Provide concise, helpful feedback."
            },
            {
                "role": "user",
                "content": formatted_prompt
            }
        ],
        temperature=0.7,  # Slight creativity for natural language
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
