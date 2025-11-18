from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta
import random

router = APIRouter()

class RiskMetric(BaseModel):
    category: str
    score: float
    level: str
    trend: str
    last_updated: datetime

class RiskAlert(BaseModel):
    id: str
    severity: str
    category: str
    title: str
    description: str
    recommendation: str
    created_at: datetime
    is_resolved: bool = False

class RiskTimelineEvent(BaseModel):
    date: datetime
    event_type: str
    description: str
    impact: str

class RiskDashboardData(BaseModel):
    overall_risk_score: float
    overall_risk_level: str
    risk_metrics: List[RiskMetric]
    active_alerts: List[RiskAlert]
    timeline: List[RiskTimelineEvent]
    last_updated: datetime

class RiskDashboardResponse(BaseModel):
    success: bool = True
    data: RiskDashboardData
    message: str

@router.get("/overview", response_model=RiskDashboardResponse)
async def get_risk_overview():
    """
    Get comprehensive risk dashboard overview with all risk dimensions.
    """
    risk_metrics = [
        RiskMetric(
            category="Business Health",
            score=65.0,
            level="medium",
            trend="declining",
            last_updated=datetime.utcnow()
        ),
        RiskMetric(
            category="Cyber Security",
            score=45.0,
            level="high",
            trend="stable",
            last_updated=datetime.utcnow()
        ),
        RiskMetric(
            category="Financial",
            score=55.0,
            level="medium",
            trend="improving",
            last_updated=datetime.utcnow()
        ),
        RiskMetric(
            category="Legal/Compliance",
            score=30.0,
            level="low",
            trend="stable",
            last_updated=datetime.utcnow()
        ),
        RiskMetric(
            category="Market",
            score=50.0,
            level="medium",
            trend="declining",
            last_updated=datetime.utcnow()
        )
    ]
    
    overall_score = sum(m.score for m in risk_metrics) / len(risk_metrics)
    
    if overall_score >= 70:
        overall_level = "critical"
    elif overall_score >= 50:
        overall_level = "high"
    elif overall_score >= 30:
        overall_level = "medium"
    else:
        overall_level = "low"
    
    active_alerts = [
        RiskAlert(
            id="alert_001",
            severity="high",
            category="cyber",
            title="Data Breach Detected",
            description="Email found in recent data breach",
            recommendation="Change passwords and enable 2FA immediately",
            created_at=datetime.utcnow() - timedelta(hours=2),
            is_resolved=False
        ),
        RiskAlert(
            id="alert_002",
            severity="medium",
            category="financial",
            title="Cash Flow Warning",
            description="Negative cash flow trend detected",
            recommendation="Review expenses and accelerate receivables",
            created_at=datetime.utcnow() - timedelta(days=1),
            is_resolved=False
        ),
        RiskAlert(
            id="alert_003",
            severity="medium",
            category="legal",
            title="Contract Risk Identified",
            description="Unfair termination clause in supplier contract",
            recommendation="Renegotiate contract terms before renewal",
            created_at=datetime.utcnow() - timedelta(days=3),
            is_resolved=False
        )
    ]
    
    timeline = [
        RiskTimelineEvent(
            date=datetime.utcnow() - timedelta(hours=2),
            event_type="threat_detected",
            description="Data breach exposure identified",
            impact="high"
        ),
        RiskTimelineEvent(
            date=datetime.utcnow() - timedelta(days=1),
            event_type="risk_increased",
            description="Cash flow risk elevated to medium",
            impact="medium"
        ),
        RiskTimelineEvent(
            date=datetime.utcnow() - timedelta(days=3),
            event_type="contract_analyzed",
            description="Supplier contract analysis completed",
            impact="medium"
        ),
        RiskTimelineEvent(
            date=datetime.utcnow() - timedelta(days=7),
            event_type="risk_decreased",
            description="Cyber security score improved",
            impact="positive"
        )
    ]
    
    dashboard_data = RiskDashboardData(
        overall_risk_score=round(overall_score, 2),
        overall_risk_level=overall_level,
        risk_metrics=risk_metrics,
        active_alerts=active_alerts,
        timeline=timeline,
        last_updated=datetime.utcnow()
    )
    
    return RiskDashboardResponse(
        success=True,
        data=dashboard_data,
        message="Risk dashboard data retrieved successfully"
    )

@router.get("/alerts")
async def get_active_alerts():
    """
    Get all active risk alerts.
    """
    return {
        "success": True,
        "data": {
            "total_alerts": 3,
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 0
        },
        "message": "Active alerts retrieved"
    }

@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """
    Mark an alert as resolved.
    """
    return {
        "success": True,
        "data": {
            "alert_id": alert_id,
            "status": "resolved",
            "resolved_at": datetime.utcnow()
        },
        "message": "Alert resolved successfully"
    }
