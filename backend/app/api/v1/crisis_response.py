from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import openai

from app.core.config import settings

router = APIRouter()

class CrisisRequest(BaseModel):
    crisis_type: str = Field(..., description="Type: cash_flow, data_breach, legal, customer_loss, reputation, market_shift")
    description: str = Field(..., description="Description of the crisis")
    severity: Optional[str] = Field("medium", description="Severity: low, medium, high, critical")
    context: Optional[dict] = Field(None, description="Additional context")

class CrisisStep(BaseModel):
    step_number: int
    title: str
    description: str
    priority: str
    timeframe: str
    resources_needed: List[str]

class CrisisPlaybook(BaseModel):
    crisis_type: str
    severity: str
    immediate_actions: List[str]
    steps: List[CrisisStep]
    resources: List[str]
    contacts: List[str]
    estimated_resolution_time: str
    generated_at: datetime

class CrisisResponse(BaseModel):
    success: bool = True
    data: CrisisPlaybook
    message: str

@router.post("/generate-playbook", response_model=CrisisResponse)
async def generate_crisis_playbook(request: CrisisRequest):
    """
    Generate AI-powered crisis response playbook with step-by-step guidance.
    """
    try:
        if settings.OPENAI_API_KEY:
            playbook = await generate_ai_playbook(request)
        else:
            playbook = generate_template_playbook(request)
        
        return CrisisResponse(
            success=True,
            data=playbook,
            message="Crisis response playbook generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Playbook generation failed: {str(e)}")

async def generate_ai_playbook(request: CrisisRequest) -> CrisisPlaybook:
    """Generate crisis playbook using GPT-4."""
    
    prompt = f"""You are a business crisis management expert. Generate a detailed crisis response playbook for the following situation:

Crisis Type: {request.crisis_type}
Severity: {request.severity}
Description: {request.description}

Provide a comprehensive, actionable playbook in JSON format with:
1. Immediate actions (first 24 hours)
2. Step-by-step response plan (5-7 steps)
3. Required resources
4. Key contacts to notify
5. Estimated resolution timeframe

Focus on practical, actionable steps that a small business owner can implement immediately.

JSON format:
{{
    "immediate_actions": ["action1", "action2", "action3"],
    "steps": [
        {{
            "step_number": 1,
            "title": "Step title",
            "description": "Detailed description",
            "priority": "critical|high|medium",
            "timeframe": "immediate|24h|1week|ongoing",
            "resources_needed": ["resource1", "resource2"]
        }}
    ],
    "resources": ["resource1", "resource2"],
    "contacts": ["contact1", "contact2"],
    "estimated_resolution_time": "timeframe"
}}"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert business crisis management consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        import json
        import re
        result_text = response.choices[0].message.content
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            result_json = json.loads(json_match.group())
        else:
            result_json = json.loads(result_text)
        
        steps = [CrisisStep(**step) for step in result_json.get("steps", [])]
        
        return CrisisPlaybook(
            crisis_type=request.crisis_type,
            severity=request.severity,
            immediate_actions=result_json.get("immediate_actions", []),
            steps=steps,
            resources=result_json.get("resources", []),
            contacts=result_json.get("contacts", []),
            estimated_resolution_time=result_json.get("estimated_resolution_time", "Unknown"),
            generated_at=datetime.utcnow()
        )
    except Exception as e:
        print(f"AI playbook generation failed: {e}")
        return generate_template_playbook(request)

def generate_template_playbook(request: CrisisRequest) -> CrisisPlaybook:
    """Generate template-based crisis playbook."""
    
    playbooks = {
        "cash_flow": {
            "immediate_actions": [
                "Review all outstanding invoices and accelerate collection",
                "Identify non-essential expenses that can be cut immediately",
                "Contact key suppliers to negotiate payment terms"
            ],
            "steps": [
                CrisisStep(
                    step_number=1,
                    title="Emergency Cash Flow Assessment",
                    description="Calculate exact cash position and runway. List all receivables and payables.",
                    priority="critical",
                    timeframe="immediate",
                    resources_needed=["Financial statements", "Bank statements", "AR/AP reports"]
                ),
                CrisisStep(
                    step_number=2,
                    title="Expense Reduction Plan",
                    description="Cut all non-essential expenses. Renegotiate contracts. Delay discretionary spending.",
                    priority="critical",
                    timeframe="24h",
                    resources_needed=["Expense report", "Vendor contracts"]
                ),
                CrisisStep(
                    step_number=3,
                    title="Revenue Acceleration",
                    description="Contact all customers with outstanding invoices. Offer early payment discounts.",
                    priority="high",
                    timeframe="24-48h",
                    resources_needed=["Customer list", "Invoice system"]
                ),
                CrisisStep(
                    step_number=4,
                    title="Emergency Funding Options",
                    description="Explore bridge loans, invoice factoring, or emergency investor funding.",
                    priority="high",
                    timeframe="1 week",
                    resources_needed=["Financial projections", "Business plan"]
                ),
                CrisisStep(
                    step_number=5,
                    title="Stakeholder Communication",
                    description="Inform key stakeholders (team, investors, board) of situation and action plan.",
                    priority="medium",
                    timeframe="48h",
                    resources_needed=["Communication plan", "Financial summary"]
                )
            ],
            "resources": ["Accountant", "Financial advisor", "Legal counsel", "Bank relationship manager"],
            "contacts": ["Accountant", "Bank", "Key investors", "Business attorney"],
            "estimated_resolution_time": "2-4 weeks"
        },
        "data_breach": {
            "immediate_actions": [
                "Isolate affected systems immediately",
                "Change all passwords and revoke compromised credentials",
                "Notify IT security team or consultant"
            ],
            "steps": [
                CrisisStep(
                    step_number=1,
                    title="Contain the Breach",
                    description="Disconnect affected systems. Preserve evidence. Stop data exfiltration.",
                    priority="critical",
                    timeframe="immediate",
                    resources_needed=["IT team", "Security tools", "Backup systems"]
                ),
                CrisisStep(
                    step_number=2,
                    title="Assess Impact",
                    description="Determine what data was accessed, how many users affected, and extent of compromise.",
                    priority="critical",
                    timeframe="24h",
                    resources_needed=["Security logs", "Forensic tools", "IT expertise"]
                ),
                CrisisStep(
                    step_number=3,
                    title="Legal Compliance",
                    description="Notify authorities as required by GDPR/CCPA. Document everything.",
                    priority="high",
                    timeframe="72h",
                    resources_needed=["Legal counsel", "Compliance officer"]
                ),
                CrisisStep(
                    step_number=4,
                    title="Customer Notification",
                    description="Inform affected customers. Provide credit monitoring if needed.",
                    priority="high",
                    timeframe="72h",
                    resources_needed=["Communication plan", "PR support"]
                ),
                CrisisStep(
                    step_number=5,
                    title="Security Remediation",
                    description="Fix vulnerabilities. Implement additional security measures. Conduct security audit.",
                    priority="high",
                    timeframe="1-2 weeks",
                    resources_needed=["Security consultant", "IT infrastructure"]
                )
            ],
            "resources": ["Cybersecurity consultant", "Legal counsel", "PR firm", "Forensics team"],
            "contacts": ["IT security team", "Legal counsel", "Law enforcement", "Data protection authority"],
            "estimated_resolution_time": "2-6 weeks"
        },
        "customer_loss": {
            "immediate_actions": [
                "Contact churned customers to understand reasons",
                "Analyze churn patterns and identify at-risk customers",
                "Implement immediate retention offers for at-risk customers"
            ],
            "steps": [
                CrisisStep(
                    step_number=1,
                    title="Churn Analysis",
                    description="Analyze why customers are leaving. Identify common patterns and root causes.",
                    priority="high",
                    timeframe="24-48h",
                    resources_needed=["Customer data", "Analytics tools", "Feedback surveys"]
                ),
                CrisisStep(
                    step_number=2,
                    title="At-Risk Customer Identification",
                    description="Identify customers showing churn signals. Prioritize high-value accounts.",
                    priority="high",
                    timeframe="48h",
                    resources_needed=["CRM data", "Usage analytics"]
                ),
                CrisisStep(
                    step_number=3,
                    title="Retention Campaign",
                    description="Launch targeted retention campaign with special offers and personalized outreach.",
                    priority="high",
                    timeframe="1 week",
                    resources_needed=["Marketing team", "Special offers", "Communication tools"]
                ),
                CrisisStep(
                    step_number=4,
                    title="Product/Service Improvement",
                    description="Address root causes identified in churn analysis. Fix product issues.",
                    priority="medium",
                    timeframe="2-4 weeks",
                    resources_needed=["Product team", "Development resources"]
                ),
                CrisisStep(
                    step_number=5,
                    title="Customer Success Program",
                    description="Implement proactive customer success program to prevent future churn.",
                    priority="medium",
                    timeframe="ongoing",
                    resources_needed=["Customer success team", "Monitoring tools"]
                )
            ],
            "resources": ["Customer success team", "Marketing team", "Product team", "Analytics tools"],
            "contacts": ["Customer success manager", "Product manager", "Marketing lead"],
            "estimated_resolution_time": "4-8 weeks"
        }
    }
    
    template = playbooks.get(request.crisis_type, playbooks["cash_flow"])
    
    return CrisisPlaybook(
        crisis_type=request.crisis_type,
        severity=request.severity,
        immediate_actions=template["immediate_actions"],
        steps=template["steps"],
        resources=template["resources"],
        contacts=template["contacts"],
        estimated_resolution_time=template["estimated_resolution_time"],
        generated_at=datetime.utcnow()
    )

@router.get("/demo")
async def get_demo_playbook():
    """
    Get a demo crisis response playbook.
    """
    demo_request = CrisisRequest(
        crisis_type="cash_flow",
        description="Negative cash flow for 3 consecutive months, runway less than 2 months",
        severity="high"
    )
    return await generate_crisis_playbook(demo_request)

@router.get("/crisis-types")
async def get_crisis_types():
    """
    Get list of supported crisis types.
    """
    return {
        "success": True,
        "data": {
            "crisis_types": [
                {"id": "cash_flow", "name": "Cash Flow Crisis", "description": "Negative cash flow, low runway"},
                {"id": "data_breach", "name": "Data Breach", "description": "Security breach, data exposure"},
                {"id": "legal", "name": "Legal Issue", "description": "Lawsuits, compliance violations"},
                {"id": "customer_loss", "name": "Customer Churn", "description": "High customer attrition"},
                {"id": "reputation", "name": "Reputation Crisis", "description": "PR issues, negative publicity"},
                {"id": "market_shift", "name": "Market Disruption", "description": "Sudden market changes"}
            ]
        },
        "message": "Crisis types retrieved"
    }
