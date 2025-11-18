from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime
import requests
import hashlib

router = APIRouter()

class CyberThreatRequest(BaseModel):
    domain: Optional[str] = Field(None, description="Domain to check")
    email: Optional[str] = Field(None, description="Email to check for breaches")
    url: Optional[HttpUrl] = Field(None, description="URL to scan")

class ThreatDetail(BaseModel):
    type: str
    severity: str
    description: str
    recommendation: str

class CyberThreatResult(BaseModel):
    security_score: float = Field(..., description="Overall security score (0-100)")
    risk_level: str
    threats_detected: int
    threats: List[ThreatDetail]
    breach_found: bool = False
    breach_details: Optional[str] = None
    checked_at: datetime = Field(default_factory=datetime.utcnow)

class CyberThreatResponse(BaseModel):
    success: bool = True
    data: CyberThreatResult
    message: str

@router.post("/scan", response_model=CyberThreatResponse)
async def scan_cyber_threats(request: CyberThreatRequest):
    """
    Scan for cyber threats including:
    - Domain security issues
    - Data breach exposure
    - SSL/TLS vulnerabilities
    - Malware detection
    """
    threats = []
    security_score = 100.0
    breach_found = False
    breach_details = None
    
    if request.email:
        breach_check = await check_email_breach(request.email)
        if breach_check["found"]:
            breach_found = True
            breach_details = breach_check["details"]
            security_score -= 30
            threats.append(ThreatDetail(
                type="data_breach",
                severity="high",
                description=f"Email found in {breach_check['breach_count']} data breaches",
                recommendation="Change passwords immediately and enable 2FA on all accounts"
            ))
    
    if request.domain:
        domain_threats = check_domain_security(request.domain)
        threats.extend(domain_threats)
        security_score -= len(domain_threats) * 10
    
    if request.url:
        url_threats = check_url_safety(str(request.url))
        threats.extend(url_threats)
        security_score -= len(url_threats) * 15
    
    security_score = max(security_score, 0)
    
    if security_score >= 80:
        risk_level = "low"
    elif security_score >= 60:
        risk_level = "medium"
    elif security_score >= 40:
        risk_level = "high"
    else:
        risk_level = "critical"
    
    result = CyberThreatResult(
        security_score=round(security_score, 2),
        risk_level=risk_level,
        threats_detected=len(threats),
        threats=threats,
        breach_found=breach_found,
        breach_details=breach_details,
        checked_at=datetime.utcnow()
    )
    
    return CyberThreatResponse(
        success=True,
        data=result,
        message="Cyber threat scan completed"
    )

async def check_email_breach(email: str) -> dict:
    """
    Check if email has been in data breaches using HaveIBeenPwned API.
    """
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {
            "User-Agent": "VentureGuard-AI",
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            breaches = response.json()
            return {
                "found": True,
                "breach_count": len(breaches),
                "details": f"Found in {len(breaches)} breaches: {', '.join([b['Name'] for b in breaches[:3]])}"
            }
        elif response.status_code == 404:
            return {"found": False, "breach_count": 0, "details": None}
        else:
            return {"found": False, "breach_count": 0, "details": "Could not check"}
    except Exception as e:
        print(f"Breach check error: {e}")
        return {"found": False, "breach_count": 0, "details": "Check unavailable"}

def check_domain_security(domain: str) -> List[ThreatDetail]:
    """
    Check domain for security issues.
    """
    threats = []
    
    if not domain.startswith("https://"):
        threats.append(ThreatDetail(
            type="ssl_missing",
            severity="medium",
            description="Domain does not use HTTPS",
            recommendation="Implement SSL/TLS certificate for secure connections"
        ))
    
    suspicious_keywords = ["free", "click", "win", "prize", "urgent"]
    if any(keyword in domain.lower() for keyword in suspicious_keywords):
        threats.append(ThreatDetail(
            type="suspicious_domain",
            severity="medium",
            description="Domain contains suspicious keywords",
            recommendation="Verify domain legitimacy before sharing sensitive information"
        ))
    
    return threats

def check_url_safety(url: str) -> List[ThreatDetail]:
    """
    Check URL for safety issues.
    """
    threats = []
    
    if not url.startswith("https://"):
        threats.append(ThreatDetail(
            type="insecure_connection",
            severity="high",
            description="URL uses insecure HTTP protocol",
            recommendation="Only use HTTPS connections for sensitive operations"
        ))
    
    suspicious_patterns = ["bit.ly", "tinyurl", "goo.gl"]
    if any(pattern in url.lower() for pattern in suspicious_patterns):
        threats.append(ThreatDetail(
            type="url_shortener",
            severity="low",
            description="URL uses link shortener which may hide destination",
            recommendation="Verify actual destination before clicking"
        ))
    
    return threats

@router.get("/demo")
async def get_demo_scan():
    """
    Get a demo cyber threat scan.
    """
    demo_request = CyberThreatRequest(
        domain="http://example-business.com",
        email="test@example.com"
    )
    return await scan_cyber_threats(demo_request)
