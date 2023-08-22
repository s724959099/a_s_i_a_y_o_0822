from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_correct_conversion():
    response = client.get(
        "/api/currency/_convert_currency",
        params={"source": "USD", "target": "JPY", "amount": "$1,525"},
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 1525 * 111.801


def test_invalid_amount():
    response = client.get(
        "/api/currency/_convert_currency",
        params={"source": "XYZ", "target": "JPY", "amount": "$1,525"},
    )
    assert response.status_code == 400


def test_invalid_currency_code():
    response = client.get(
        "/api/currency/_convert_currency?source=INVALID&target=JPY&amount=$1,525",
        params={"source": "USD", "target": "JPY", "amount": "$1252"},
    )
    assert response.status_code == 400
