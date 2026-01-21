
"""
Credit Worthiness Assessment API
FastAPI Backend
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas.credit import ExtractResponse, PredictRequest, PredictResponse, FeedbackRequest, FeedbackResponse
from services.extractor import extract_from_text, parse_csv_content, parse_pdf_content
from services.feedback import generate_feedback
from models.predictor import predict

# Create app
app = FastAPI(
    title="Credit Worthiness Assessment API",
    description="API for assessing credit worthiness using ML predictions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """API info endpoint."""
    return {
        "name": "Credit Worthiness Assessment API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "extract": "/extract (POST)",
            "predict": "/predict (POST)",
            "feedback": "/feedback (POST)"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/extract", response_model=ExtractResponse)
async def extract_financial_data(file: UploadFile = File(...)):
    """
    Extract financial variables from uploaded bank statement.
    Accepts PDF or CSV files.
    """
    # Validate file type
    filename = file.filename.lower()
    if not (filename.endswith(".pdf") or filename.endswith(".csv")):
        raise HTTPException(status_code=400, detail="Only PDF and CSV files are supported")

    try:
        content = await file.read()

        if filename.endswith(".csv"):
            text = parse_csv_content(content.decode("utf-8"))
            file_type = "CSV"
        else:
            text = parse_pdf_content(content)
            file_type = "PDF"

        # Extract using OpenAI
        result = extract_from_text(text, file_type)

        return ExtractResponse(**result)

    except Exception as e:
        import traceback
        print(f"Extraction error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@app.post("/predict", response_model=PredictResponse)
def predict_credit(request: PredictRequest):
    """
    Predict credit worthiness.
    Returns credit score, default probability, and risk category.
    """
    try:
        # Convert request to dict for prediction
        data = request.model_dump()

        # Get prediction
        result = predict(data)

        return PredictResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/feedback", response_model=FeedbackResponse)
def get_feedback(request: FeedbackRequest):
    """
    Generate AI-powered personalized feedback based on assessment results.
    """
    try:
        # Separate user data and results
        user_data = {
            "name": request.name,
            "age": request.age,
            "employment_status": request.employment_status,
            "total_monthly_inflow": request.total_monthly_inflow,
            "total_monthly_outflow": request.total_monthly_outflow,
            "end_of_month_balance": request.end_of_month_balance,
            "salary_payment_detected": request.salary_payment_detected,
            "transaction_frequency": request.transaction_frequency,
            "gambling_transactions_count": request.gambling_transactions_count,
            "previous_loan_taken": request.previous_loan_taken,
            "repayment_status": request.repayment_status,
            "missed_payment_count": request.missed_payment_count,
        }

        results = {
            "credit_score": request.credit_score,
            "risk_category": request.risk_category,
            "default_probability": request.default_probability,
        }

        feedback = generate_feedback(user_data, results)

        return FeedbackResponse(feedback=feedback)

    except Exception as e:
        import traceback
        print(f"Feedback generation error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Feedback generation failed: {str(e)}")
