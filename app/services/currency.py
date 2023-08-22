import json
import os
import re

from schemas.currency import Currencies


class CurrencyData:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.data = {}

            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(dir_path, "../data/currencies.json")) as f:
                cls.__instance.data = json.load(f)["currencies"]
        return cls.__instance


def get_currencies() -> Currencies:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "../data/currencies.json")) as f:
        return json.load(f)["currencies"]


def validate_amount(amount: str):
    if not re.match(r"^\$(0|[1-9][0-9]{0,2})(,\d{3})*(\.\d{1,2})?$", amount):
        raise ValueError(f"Invalid amount format: {amount}")
    return float(amount.replace(",", "").replace("$", ""))


def validate_currency_code(code: str, currencies: Currencies):
    if code not in currencies:
        raise KeyError(f"Invalid currency code: {code}")
    return code


def convert_currency(currencies, amount: str, source: str, target: str):
    amount = validate_amount(amount)
    source = validate_currency_code(source, currencies)
    target = validate_currency_code(target, currencies)
    result = amount * currencies[source][target]
    return result
