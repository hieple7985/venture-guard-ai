from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class ContractAnalysisRequest(BaseModel):
    contract_text: str = Field(..., description="Contract text to analyze")
    contract_type: Optional[str] = Field(None, description="Type: supplier, client, partnership, employment")

class ContractIssue(BaseModel):
    severity: str = Field(..., description="Severity: critical, high, medium, low")
    category: str = Field(..., description="Category: legal, financial, liability, termination, etc")
    issue: str = Field(..., description="Description of the issue")
    location: str = Field(..., description="Where in contract this appears")
    recommendation: str = Field(..., description="Suggested action")

class ContractAnalysisResult(BaseModel):
    overall_risk_score: float = Field(..., description="Overall risk score (0-100)")
    risk_level: str = Field(..., description="Risk level: low, medium, high, critical")
    issues: List[ContractIssue] = Field(..., description="List of identified issues")
    positive_aspects: List[str] = Field(..., description="Favorable terms found")
    missing_clauses: List[str] = Field(..., description="Important missing clauses")
    summary: str = Field(..., description="Executive summary")
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)

class ContractAnalysisResponse(BaseModel):
    success: bool = True
    data: ContractAnalysisResult
    message: str = "Contract analysis completed"
