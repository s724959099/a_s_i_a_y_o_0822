from fastapi import APIRouter

from .endpoints import currency

router = APIRouter()
router.include_router(currency.router, prefix="/currency", tags=["currency"])
