from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from schemas.currency import CurrencyQuery
from services.currency import convert_currency, get_currencies

router = APIRouter()


@router.get("/_convert_currency")
async def get_convert_currency(query: CurrencyQuery = Depends()):
    try:
        currencies = get_currencies()
        result = convert_currency(currencies, query.amount, query.source, query.target)
        return {"msg": "success", "amount": result}
    except (ValueError, KeyError) as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "fail", "error": str(e)}
        )
