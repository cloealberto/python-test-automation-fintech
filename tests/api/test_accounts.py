import requests


def test_create_account_success(base_url: str, http: requests.Session):
    """
    Happy path: criar conta com saldo inicial válido.
    """
    response = http.post(
        f"{base_url}/accounts",
        json={"owner_name": "QA Test User", "initial_balance": 500},
        timeout=10,
    )

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["owner_name"] == "QA Test User"
    assert float(data["balance"]) == 500.0


def test_create_account_rejects_negative_balance(base_url: str, http: requests.Session):
    """
    Validação: saldo inicial não pode ser negativo.
    Espera 422 (validação do Pydantic).
    """
    response = http.post(
        f"{base_url}/accounts",
        json={"owner_name": "User", "initial_balance": -1},
        timeout=10,
    )

    assert response.status_code == 422


def test_get_balance_success(base_url: str, http: requests.Session, create_account):
    """
    Cria uma conta e consulta saldo.
    """
    created = create_account("Balance User", 123.45)
    assert created.status_code == 201

    account_id = created.json()["id"]

    response = http.get(f"{base_url}/accounts/{account_id}/balance", timeout=10)
    assert response.status_code == 200

    payload = response.json()
    assert payload["account_id"] == account_id
    assert float(payload["balance"]) == 123.45


def test_get_balance_not_found(base_url: str, http: requests.Session):
    """
    Consulta saldo de conta inexistente -> 404
    """
    response = http.get(f"{base_url}/accounts/999999/balance", timeout=10)
    assert response.status_code == 404