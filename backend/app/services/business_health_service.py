import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

from app.schemas.business_health import BusinessMetrics, RiskPrediction

class BusinessHealthService:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def predict_business_health(self, metrics: BusinessMetrics) -> RiskPrediction:
        """
        Predict business health and risks using AI/ML models.
        """
        revenue = np.array(metrics.monthly_revenue)
        expenses = np.array(metrics.monthly_expenses)
        cash_flow = revenue - expenses
        
        cash_flow_risk = self._calculate_cash_flow_risk(cash_flow, revenue, expenses)
        market_risk = self._calculate_market_risk(revenue, metrics)
        operational_risk = self._calculate_operational_risk(metrics)
        
        overall_risk = (cash_flow_risk * 0.5 + market_risk * 0.3 + operational_risk * 0.2)
        
        risk_level = self._get_risk_level(overall_risk)
        
        predictions = self._generate_predictions(cash_flow, revenue, expenses, metrics)
        recommendations = self._generate_recommendations(
            overall_risk, cash_flow_risk, market_risk, operational_risk, predictions
        )
        
        return RiskPrediction(
            risk_score=round(overall_risk, 2),
            risk_level=risk_level,
            cash_flow_risk=round(cash_flow_risk, 2),
            market_risk=round(market_risk, 2),
            operational_risk=round(operational_risk, 2),
            predictions=predictions,
            recommendations=recommendations,
            predicted_at=datetime.utcnow()
        )
    
    def _calculate_cash_flow_risk(self, cash_flow: np.ndarray, revenue: np.ndarray, expenses: np.ndarray) -> float:
        """Calculate cash flow risk score (0-100)."""
        if len(cash_flow) < 3:
            return 50.0
        
        risk_score = 0.0
        
        negative_months = np.sum(cash_flow < 0)
        if negative_months > 0:
            risk_score += (negative_months / len(cash_flow)) * 40
        
        trend = np.polyfit(range(len(cash_flow)), cash_flow, 1)[0]
        if trend < 0:
            risk_score += min(abs(trend) / np.mean(np.abs(cash_flow)) * 30, 30)
        
        recent_cash_flow = cash_flow[-3:]
        if np.mean(recent_cash_flow) < 0:
            risk_score += 20
        
        burn_rate = np.mean(expenses[-3:])
        avg_cash_flow = np.mean(cash_flow[-3:])
        if avg_cash_flow > 0:
            runway_months = avg_cash_flow / burn_rate * 12
            if runway_months < 3:
                risk_score += 10
        
        return min(risk_score, 100.0)
    
    def _calculate_market_risk(self, revenue: np.ndarray, metrics: BusinessMetrics) -> float:
        """Calculate market risk score (0-100)."""
        risk_score = 0.0
        
        if len(revenue) >= 3:
            revenue_trend = np.polyfit(range(len(revenue)), revenue, 1)[0]
            if revenue_trend < 0:
                risk_score += min(abs(revenue_trend) / np.mean(revenue) * 40, 40)
        
        if len(revenue) >= 2:
            recent_decline = (revenue[-1] - revenue[-2]) / revenue[-2]
            if recent_decline < -0.1:
                risk_score += 20
        
        if metrics.customer_churn_rate and metrics.customer_churn_rate > 0.05:
            risk_score += min(metrics.customer_churn_rate * 200, 30)
        
        if metrics.business_age_months and metrics.business_age_months < 12:
            risk_score += 10
        
        return min(risk_score, 100.0)
    
    def _calculate_operational_risk(self, metrics: BusinessMetrics) -> float:
        """Calculate operational risk score (0-100)."""
        risk_score = 30.0
        
        if metrics.employee_count:
            if metrics.employee_count < 3:
                risk_score += 20
            elif metrics.employee_count > 50:
                risk_score -= 10
        
        if metrics.business_age_months:
            if metrics.business_age_months < 6:
                risk_score += 20
            elif metrics.business_age_months > 24:
                risk_score -= 10
        
        return max(min(risk_score, 100.0), 0.0)
    
    def _generate_predictions(self, cash_flow: np.ndarray, revenue: np.ndarray, 
                            expenses: np.ndarray, metrics: BusinessMetrics) -> Dict:
        """Generate specific predictions for the next 30-90 days."""
        predictions = {}
        
        if len(cash_flow) >= 3:
            trend = np.polyfit(range(len(cash_flow)), cash_flow, 1)[0]
            next_month_cf = cash_flow[-1] + trend
            predictions["next_month_cash_flow"] = float(round(next_month_cf, 2))
            predictions["cash_flow_trend"] = "declining" if trend < 0 else "improving"
        
        if len(revenue) >= 3:
            revenue_trend = np.polyfit(range(len(revenue)), revenue, 1)[0]
            predictions["revenue_trend"] = "declining" if revenue_trend < 0 else "growing"
            predictions["projected_revenue_change"] = f"{round(revenue_trend / np.mean(revenue) * 100, 1)}%"
        
        avg_cash_flow = np.mean(cash_flow[-3:]) if len(cash_flow) >= 3 else cash_flow[-1]
        avg_expenses = np.mean(expenses[-3:]) if len(expenses) >= 3 else expenses[-1]
        
        if avg_cash_flow > 0:
            runway_months = (avg_cash_flow * len(cash_flow)) / avg_expenses
            predictions["runway_months"] = round(runway_months, 1)
        else:
            predictions["runway_months"] = 0
            predictions["cash_crisis_warning"] = "Immediate action required"
        
        if metrics.customer_churn_rate:
            if metrics.customer_count:
                expected_churn = metrics.customer_count * metrics.customer_churn_rate
                predictions["expected_customer_loss_30d"] = int(expected_churn)
        
        return predictions
    
    def _generate_recommendations(self, overall_risk: float, cash_flow_risk: float,
                                 market_risk: float, operational_risk: float,
                                 predictions: Dict) -> List[str]:
        """Generate actionable recommendations based on risk analysis."""
        recommendations = []
        
        if cash_flow_risk > 70:
            recommendations.append("🚨 URGENT: Cash flow crisis detected. Reduce expenses immediately and accelerate receivables collection.")
            recommendations.append("Consider emergency funding options: bridge loans, invoice factoring, or emergency investor funding.")
        elif cash_flow_risk > 50:
            recommendations.append("⚠️ Cash flow concerns detected. Review and optimize expense structure within 30 days.")
            recommendations.append("Implement stricter payment terms and improve collection processes.")
        
        if market_risk > 60:
            recommendations.append("📉 Market risk is high. Diversify revenue streams and explore new customer segments.")
            recommendations.append("Conduct competitive analysis and adjust pricing/positioning strategy.")
        
        if predictions.get("runway_months", 12) < 3:
            recommendations.append("⏰ Critical: Less than 3 months runway. Secure funding or drastically cut costs immediately.")
        elif predictions.get("runway_months", 12) < 6:
            recommendations.append("⚠️ Low runway (< 6 months). Start fundraising process or implement cost reduction plan.")
        
        if predictions.get("cash_flow_trend") == "declining":
            recommendations.append("📊 Declining cash flow trend. Analyze and address root causes: pricing, costs, or market conditions.")
        
        if operational_risk > 60:
            recommendations.append("🔧 Operational risk elevated. Consider hiring key personnel or improving processes.")
        
        if overall_risk < 30:
            recommendations.append("✅ Business health is good. Focus on growth and scaling operations.")
            recommendations.append("Consider investing in marketing, product development, or team expansion.")
        
        if not recommendations:
            recommendations.append("📈 Continue monitoring key metrics and maintain current trajectory.")
        
        return recommendations
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to risk level."""
        if risk_score >= 75:
            return "critical"
        elif risk_score >= 50:
            return "high"
        elif risk_score >= 25:
            return "medium"
        else:
            return "low"
