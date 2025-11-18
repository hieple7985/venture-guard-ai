import openai
from typing import List, Dict
import json
import re
from datetime import datetime

from app.core.config import settings
from app.schemas.contract import ContractAnalysisResult, ContractIssue

class ContractAnalyzerService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    async def analyze_contract(self, contract_text: str, contract_type: str = None) -> ContractAnalysisResult:
        """
        Analyze contract using GPT-4 to identify risks, unfair terms, and missing clauses.
        """
        if not settings.OPENAI_API_KEY:
            return self._fallback_analysis(contract_text)
        
        try:
            analysis = await self._gpt4_analysis(contract_text, contract_type)
            return analysis
        except Exception as e:
            print(f"GPT-4 analysis failed: {e}")
            return self._fallback_analysis(contract_text)
    
    async def _gpt4_analysis(self, contract_text: str, contract_type: str = None) -> ContractAnalysisResult:
        """Use GPT-4 to analyze contract."""
        
        prompt = f"""You are a legal AI assistant specializing in contract analysis for small businesses and entrepreneurs. 
Analyze the following contract and identify:

1. CRITICAL ISSUES: Unfair terms, hidden risks, one-sided clauses
2. LEGAL RISKS: Liability issues, termination clauses, dispute resolution
3. FINANCIAL RISKS: Payment terms, penalties, hidden costs
4. MISSING CLAUSES: Important protections that should be included
5. POSITIVE ASPECTS: Favorable terms for the entrepreneur

Contract Type: {contract_type or 'General Business Contract'}

CONTRACT TEXT:
{contract_text}

Provide your analysis in the following JSON format:
{{
    "overall_risk_score": <0-100>,
    "risk_level": "<low|medium|high|critical>",
    "issues": [
        {{
            "severity": "<critical|high|medium|low>",
            "category": "<legal|financial|liability|termination|intellectual_property|confidentiality|other>",
            "issue": "<description>",
            "location": "<section/clause reference>",
            "recommendation": "<suggested action>"
        }}
    ],
    "positive_aspects": ["<favorable term 1>", "<favorable term 2>"],
    "missing_clauses": ["<missing clause 1>", "<missing clause 2>"],
    "summary": "<executive summary of the contract analysis>"
}}

Focus on protecting the entrepreneur from unfair terms, hidden risks, and ensuring they understand all obligations."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert legal AI assistant specializing in contract analysis for entrepreneurs and small businesses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content
            
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result_json = json.loads(json_match.group())
            else:
                result_json = json.loads(result_text)
            
            issues = [ContractIssue(**issue) for issue in result_json.get("issues", [])]
            
            return ContractAnalysisResult(
                overall_risk_score=result_json.get("overall_risk_score", 50),
                risk_level=result_json.get("risk_level", "medium"),
                issues=issues,
                positive_aspects=result_json.get("positive_aspects", []),
                missing_clauses=result_json.get("missing_clauses", []),
                summary=result_json.get("summary", "Contract analysis completed"),
                analyzed_at=datetime.utcnow()
            )
            
        except Exception as e:
            print(f"GPT-4 API error: {e}")
            raise
    
    def _fallback_analysis(self, contract_text: str) -> ContractAnalysisResult:
        """
        Fallback rule-based analysis when GPT-4 is not available.
        """
        issues = []
        risk_score = 30.0
        
        red_flags = {
            "non-compete": ("high", "legal", "Non-compete clause detected"),
            "indemnif": ("high", "liability", "Indemnification clause requires review"),
            "unlimited liability": ("critical", "liability", "Unlimited liability clause found"),
            "automatic renewal": ("medium", "termination", "Automatic renewal clause detected"),
            "no termination": ("high", "termination", "Difficult termination terms"),
            "penalty": ("medium", "financial", "Penalty clauses present"),
            "late fee": ("medium", "financial", "Late fee provisions found"),
            "exclusive": ("medium", "legal", "Exclusivity clause detected"),
            "confidential": ("low", "confidentiality", "Confidentiality obligations present"),
            "intellectual property": ("medium", "intellectual_property", "IP assignment clause found"),
        }
        
        contract_lower = contract_text.lower()
        
        for keyword, (severity, category, description) in red_flags.items():
            if keyword in contract_lower:
                issues.append(ContractIssue(
                    severity=severity,
                    category=category,
                    issue=description,
                    location="Contract body",
                    recommendation=f"Review {keyword} terms carefully with legal counsel"
                ))
                
                if severity == "critical":
                    risk_score += 25
                elif severity == "high":
                    risk_score += 15
                elif severity == "medium":
                    risk_score += 10
        
        missing_clauses = []
        important_clauses = [
            "dispute resolution", "termination", "liability", "payment terms",
            "confidentiality", "intellectual property"
        ]
        
        for clause in important_clauses:
            if clause.lower() not in contract_lower:
                missing_clauses.append(f"{clause.title()} clause")
                risk_score += 5
        
        risk_score = min(risk_score, 100)
        
        if risk_score >= 75:
            risk_level = "critical"
        elif risk_score >= 50:
            risk_level = "high"
        elif risk_score >= 25:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        positive_aspects = []
        if "mutual" in contract_lower:
            positive_aspects.append("Contains mutual obligations")
        if "reasonable" in contract_lower:
            positive_aspects.append("Uses reasonable standards")
        
        summary = f"Contract analysis completed using rule-based system. Identified {len(issues)} potential issues. "
        summary += f"Overall risk level: {risk_level}. "
        if missing_clauses:
            summary += f"Missing {len(missing_clauses)} important clauses. "
        summary += "Recommend full legal review before signing."
        
        return ContractAnalysisResult(
            overall_risk_score=round(risk_score, 2),
            risk_level=risk_level,
            issues=issues,
            positive_aspects=positive_aspects,
            missing_clauses=missing_clauses,
            summary=summary,
            analyzed_at=datetime.utcnow()
        )
