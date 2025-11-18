from fastapi import APIRouter

router = APIRouter()

from .business_health import router as business_health_router
from .contract_analyzer import router as contract_router
from .cyber_monitor import router as cyber_router
from .risk_dashboard import router as risk_router
from .crisis_response import router as crisis_router

router.include_router(business_health_router, prefix="/business-health", tags=["Business Health"])
router.include_router(contract_router, prefix="/contracts", tags=["Contract Analysis"])
router.include_router(cyber_router, prefix="/cyber", tags=["Cyber Security"])
router.include_router(risk_router, prefix="/risks", tags=["Risk Dashboard"])
router.include_router(crisis_router, prefix="/crisis", tags=["Crisis Response"])
