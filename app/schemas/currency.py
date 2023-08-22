from fastapi import Query


class CurrencyQuery:
    def __init__(
        self,
        source: str = Query(..., description="Source currency code", example="JPY"),
        target: str = Query(..., description="Target currency code", example="TWD"),
        amount: str = Query(..., description="Amount to be converted", example="$100.00"),
    ):
        self.source = source
        self.target = target
        self.amount = amount


Currencies = dict[str, dict[str, float]]
