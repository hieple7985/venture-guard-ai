from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class BusinessMetrics(BaseModel):
    monthly_revenue: List[float] = Field(..., description="Monthly revenue for past 6-12 months")
    monthly_expenses: List[float] = Field(..., description="Monthly expenses for past 6-12 months")
    customer_count: Optional[int] = Field(None, description="Current customer count")
    customer_churn_rate: Optional[float] = Field(None, description="Monthly churn rate (0-1)")
    industry: Optional[str] = Field(None, description="Business industry")
    business_age_months: Optional[int] = Field(None, description="Business age in months")
    employee_count: Optional[int] = Field(None, description="Number of employees")

class RiskPrediction(BaseModel):
    risk_score: float = Field(..., description="Overall risk score (0-100)")
    risk_level: str = Field(..., description="Risk level: low, medium, high, critical")
    cash_flow_risk: float = Field(..., description="Cash flow risk score (0-100)")
    market_risk: float = Field(..., description="Market risk score (0-100)")
    operational_risk: float = Field(..., description="Operational risk score (0-100)")
    predictions: Dict[str, any] = Field(..., description="Specific predictions")
    recommendations: List[str] = Field(..., description="Actionable recommendations")
    predicted_at: datetime = Field(default_factory=datetime.utcnow)

class BusinessHealthResponse(BaseModel):
    success: bool = True
    data: RiskPrediction
    message: str = "Business health analysis completed"
