"""
Bank Statement Extraction Service using OpenAI
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

# Lazy initialization of OpenAI client
_client = None


def get_openai_client():
    """Get or create OpenAI client."""
    global _client
    if _client is None:
        from openai import OpenAI
        import httpx
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        # Create custom httpx client without proxy to avoid compatibility issues
        http_client = httpx.Client()
        _client = OpenAI(api_key=api_key, http_client=http_client)
    return _client

EXTRACTION_PROMPT = """You are a bank statement analyzer. Extract financial data from the statement below.

RULES:
1. total_monthly_inflow: Sum of all credits/deposits. Look for "Total Credit" or sum credit column.
2. total_monthly_outflow: Sum of all debits/withdrawals. Look for "Total Debit" or sum debit column.
3. transaction_frequency: Total number of transactions in the statement.
4. salary_payment_detected: "Yes" ONLY if keywords like "salary", "payroll", "wages" appear. Personal transfers do NOT count as salary.
5. end_of_month_balance: The CLOSING BALANCE or FINAL BALANCE of the account. This is different from total credits - it's the actual money left in the account. Look for "Closing Balance", "Available Balance", or the last "Balance After" entry.
6. highest_credit_amount: The single largest credit/deposit transaction (not the total).
7. highest_debit_amount: The single largest debit/withdrawal transaction (not the total).
8. gambling_transactions_count: Count transactions containing gambling keywords (bet, betting, casino, sportbet, bet9ja, betway, sportybet, betking, 1xbet, nairabet, lotto).
9. loan_related_transactions_count: Count transactions containing loan keywords (loan, fairmoney, carbon, palmcredit, branch, okash, aella, lending, credit facility).
10. extraction_confidence: "High" if data is clear, "Medium" if some inference needed, "Low" if uncertain.

Return ONLY valid JSON with these exact keys:
{
    "total_monthly_inflow": <number>,
    "total_monthly_outflow": <number>,
    "transaction_frequency": <integer>,
    "salary_payment_detected": <"Yes" or "No">,
    "end_of_month_balance": <number>,
    "highest_credit_amount": <number>,
    "highest_debit_amount": <number>,
    "gambling_transactions_count": <integer>,
    "loan_related_transactions_count": <integer>,
    "extraction_confidence": <"High", "Medium", or "Low">
}

Bank Statement:
"""


def extract_from_text(text: str, file_type: str) -> dict:
    """Extract financial variables from bank statement text using OpenAI."""
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a bank statement data extractor.

IMPORTANT DISTINCTIONS:
- "Total Credit" or "Total Inflow" = total_monthly_inflow (sum of all money received)
- "Total Debit" or "Total Outflow" = total_monthly_outflow (sum of all money spent)
- "Closing Balance" or "Final Balance" = end_of_month_balance (money left in account at end)

These are THREE DIFFERENT values. Do not confuse them."""
            },
            {
                "role": "user",
                "content": EXTRACTION_PROMPT + text
            }
        ],
        temperature=0,
        max_tokens=500,
        response_format={"type": "json_object"}
    )

    # Parse the response
    content = response.choices[0].message.content.strip()

    # Clean up response if wrapped in markdown code block
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    result = json.loads(content)
    result["source_file_type"] = file_type

    return result


def parse_csv_content(content: str) -> str:
    """Parse CSV content to readable text for extraction."""
    # CSV is already readable, just clean it up
    lines = content.strip().split("\n")
    # Limit to first 100 lines to avoid token limits
    if len(lines) > 100:
        lines = lines[:100]
    return "\n".join(lines)


def parse_pdf_content(content: bytes) -> str:
    """Extract text from PDF bytes."""
    try:
        import PyPDF2
        from io import BytesIO

        pdf_file = BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)

        text = ""
        for page in reader.pages[:10]:  # Limit to first 10 pages
            text += page.extract_text() + "\n"

        return text
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF parsing. Install with: pip install PyPDF2")
