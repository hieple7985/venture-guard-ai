from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
import pandas as pd
import numpy as np
from io import StringIO
import json

from app.schemas.business_health import BusinessMetrics, BusinessHealthResponse, RiskPrediction
from app.services.business_health_service import BusinessHealthService

router = APIRouter()
service = BusinessHealthService()

@router.post("/analyze", response_model=BusinessHealthResponse)
async def analyze_business_health(metrics: BusinessMetrics):
    """
    Analyze business health and predict risks 30-90 days ahead.
    
    This endpoint uses AI to analyze business metrics and predict:
    - Cash flow issues
    - Market risks
    - Operational risks
    - Overall business health score
    """
    try:
        prediction = service.predict_business_health(metrics)
        return BusinessHealthResponse(
            success=True,
            data=prediction,
            message="Business health analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/analyze-csv", response_model=BusinessHealthResponse)
async def analyze_from_csv(file: UploadFile = File(...)):
    """
    Analyze business health from uploaded CSV file.
    
    CSV should contain columns: date, revenue, expenses
    """
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        if 'revenue' not in df.columns or 'expenses' not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'revenue' and 'expenses' columns"
            )
        
        metrics = BusinessMetrics(
            monthly_revenue=df['revenue'].tolist(),
            monthly_expenses=df['expenses'].tolist()
        )
        
        prediction = service.predict_business_health(metrics)
        return BusinessHealthResponse(
            success=True,
            data=prediction,
            message="Business health analysis from CSV completed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV analysis failed: {str(e)}")

@router.get("/demo")
async def get_demo_analysis():
    """
    Get a demo business health analysis with sample data.
    """
    demo_metrics = BusinessMetrics(
        monthly_revenue=[50000, 52000, 48000, 45000, 43000, 40000],
        monthly_expenses=[45000, 46000, 47000, 48000, 49000, 50000],
        customer_count=150,
        customer_churn_rate=0.05,
        industry="SaaS",
        business_age_months=18,
        employee_count=8
    )
    
    prediction = service.predict_business_health(demo_metrics)
    return BusinessHealthResponse(
        success=True,
        data=prediction,
        message="Demo business health analysis"
    )
