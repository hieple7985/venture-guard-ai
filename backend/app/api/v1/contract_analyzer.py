from fastapi import APIRouter, HTTPException, UploadFile, File
import PyPDF2
from io import BytesIO

from app.schemas.contract import ContractAnalysisRequest, ContractAnalysisResponse
from app.services.contract_analyzer_service import ContractAnalyzerService

router = APIRouter()
service = ContractAnalyzerService()

@router.post("/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(request: ContractAnalysisRequest):
    """
    Analyze contract text for risks, unfair terms, and missing clauses.
    
    Uses GPT-4 to provide comprehensive legal analysis including:
    - Identification of unfair or risky terms
    - Missing important clauses
    - Recommendations for negotiation
    - Overall risk assessment
    """
    try:
        result = await service.analyze_contract(
            request.contract_text,
            request.contract_type
        )
        return ContractAnalysisResponse(
            success=True,
            data=result,
            message="Contract analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/analyze-pdf", response_model=ContractAnalysisResponse)
async def analyze_contract_pdf(
    file: UploadFile = File(...),
    contract_type: str = None
):
    """
    Analyze contract from uploaded PDF file.
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        contents = await file.read()
        pdf_reader = PyPDF2.PdfReader(BytesIO(contents))
        
        contract_text = ""
        for page in pdf_reader.pages:
            contract_text += page.extract_text()
        
        if not contract_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        result = await service.analyze_contract(contract_text, contract_type)
        return ContractAnalysisResponse(
            success=True,
            data=result,
            message="Contract PDF analysis completed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF analysis failed: {str(e)}")

@router.get("/demo")
async def get_demo_analysis():
    """
    Get a demo contract analysis with sample contract.
    """
    demo_contract = """
    SERVICE AGREEMENT
    
    This Agreement is entered into between Company A (Client) and Company B (Service Provider).
    
    1. SERVICES: Provider shall provide consulting services as requested by Client.
    
    2. PAYMENT: Client agrees to pay $5,000 per month. Late payments will incur a 10% penalty per month.
    
    3. TERM: This agreement automatically renews annually unless terminated with 90 days notice.
    
    4. LIABILITY: Provider shall indemnify and hold harmless Client from any and all claims, including unlimited liability for any damages.
    
    5. INTELLECTUAL PROPERTY: All work product created by Provider shall be owned exclusively by Client.
    
    6. NON-COMPETE: Provider agrees not to work with any competing businesses for 2 years after termination.
    
    7. CONFIDENTIALITY: Provider shall maintain strict confidentiality of all Client information indefinitely.
    """
    
    result = await service.analyze_contract(demo_contract, "service_agreement")
    return ContractAnalysisResponse(
        success=True,
        data=result,
        message="Demo contract analysis"
    )
