import re

import pytest
from schemas.currency import Currencies
from services.currency import convert_currency, validate_amount, validate_currency_code


@pytest.fixture
def currencies():
    return {
        "TWD": {"TWD": 1, "JPY": 3.669, "USD": 0.03281},
        "JPY": {"TWD": 0.26956, "JPY": 1, "USD": 0.00885},
        "USD": {"TWD": 30.444, "JPY": 111.801, "USD": 1},
    }


class TestValidateAmount:
    def invalid_amount_test_helper(self, amount: str):
        with pytest.raises(ValueError) as e_info:
            validate_amount(amount)
        assert str(e_info.value) == f"Invalid amount format: {amount}"

    def test_valid_amount(self):
        assert validate_amount("$1,000.50") == 1000.50
        assert validate_amount("$1,000") == 1000
        assert validate_amount("$100") == 100
        assert validate_amount("$0.99") == 0.99

    def test_invalid_amount(self):
        self.invalid_amount_test_helper("1000.50")
        self.invalid_amount_test_helper("1000,50")
        self.invalid_amount_test_helper("$0.990,000")
        self.invalid_amount_test_helper("$1000,50")
        self.invalid_amount_test_helper("$10000000")
        self.invalid_amount_test_helper("$0.990000")


class TestValidateCurrencyCode:
    def setup(self):
        self.currencies: Currencies = {
            "TWD": {"TWD": 1, "JPY": 3.669, "USD": 0.03281},
            "JPY": {"TWD": 0.26956, "JPY": 1, "USD": 0.00885},
            "USD": {"TWD": 30.444, "JPY": 111.801, "USD": 1},
        }

    def validate_currency_code_helper(self, valid_code: str, currencies: Currencies):
        assert validate_currency_code(valid_code, currencies) == valid_code

    def invalidate_currency_code_helper(self, invalid_code, currencies: Currencies):
        with pytest.raises(KeyError, match=f"Invalid currency code: {invalid_code}"):
            validate_currency_code(invalid_code, currencies)

    def test_validate_currency_code(self, currencies: Currencies):
        self.validate_currency_code_helper("TWD", currencies)
        self.validate_currency_code_helper("JPY", currencies)
        self.validate_currency_code_helper("USD", currencies)

    def test_invalid_currency_code(self, currencies: Currencies):
        self.invalidate_currency_code_helper("XYZ", currencies)


class TestCurrencyConversion:
    def valid_convert_currency_helper(
        self, currencies: Currencies, amount: str, source: str, target: str
    ):
        assert convert_currency(currencies, amount, source, target) == currencies[source][
            target
        ] * float(re.sub(r"[$,]", "", amount))

    def invalid_convert_currency_data_with_key_error(
        self, currencies: Currencies, amount: str, source: str, target: str
    ):
        with pytest.raises(KeyError) as e_info:
            convert_currency(currencies, amount, source, target)
        error_message = str(e_info.value).replace("'", "")
        assert (
            error_message == f"Invalid currency code: {source}"
            or error_message == f"Invalid currency code: {target}"
        )

    def invalid_convert_currency_data_with_value_error(
        self, currencies: Currencies, amount: str, source: str, target: str
    ):
        with pytest.raises(ValueError) as e_info:
            convert_currency(currencies, amount, source, target)
        error_message = str(e_info.value)
        assert error_message == f"Invalid amount format: {amount}"

    def test_convert_valid_data(self, currencies: Currencies):
        self.valid_convert_currency_helper(currencies, "$100", "TWD", "JPY")
        self.valid_convert_currency_helper(currencies, "$2,100.01", "TWD", "JPY")
        self.valid_convert_currency_helper(currencies, "$100", "JPY", "TWD")
        self.valid_convert_currency_helper(currencies, "$2,100.01", "JPY", "TWD")

    def test_invalid_convert_currency_data_with_key_error(self, currencies: Currencies):
        self.invalid_convert_currency_data_with_key_error(currencies, "$100", "XYZ", "JPY")
        self.invalid_convert_currency_data_with_key_error(currencies, "$100", "JPY", "XYZ")

    def test_invalid_convert_currency_data_with_value_error(self, currencies: Currencies):
        self.invalid_convert_currency_data_with_value_error(currencies, "$1000000", "TWD", "JPY")
        self.invalid_convert_currency_data_with_value_error(currencies, "$100.00f", "JPY", "XYZ")
        self.invalid_convert_currency_data_with_value_error(currencies, "$100,0", "JPY", "XYZ")
        self.invalid_convert_currency_data_with_value_error(currencies, "$52.", "JPY", "XYZ")
        self.invalid_convert_currency_data_with_value_error(currencies, "$0.9990000", "JPY", "XYZ")
