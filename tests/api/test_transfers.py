import requests


def test_transfer_success_updates_balances(base_url: str, http: requests.Session, two_accounts):
    """
    Happy path:
    - cria 2 contas
    - transfere
    - valida saldos após operação
    """
    from_id, to_id = two_accounts

    # Faz transferência
    transfer = http.post(
        f"{base_url}/transfers",
        json={"from_account_id": from_id, "to_account_id": to_id, "amount": 25.0},
        timeout=10,
    )
    assert transfer.status_code == 201, transfer.text

    # Valida saldos
    b1 = http.get(f"{base_url}/accounts/{from_id}/balance", timeout=10).json()
    b2 = http.get(f"{base_url}/accounts/{to_id}/balance", timeout=10).json()

    assert float(b1["balance"]) == 75.0
    assert float(b2["balance"]) == 35.0


def test_transfer_rejects_insufficient_balance(base_url: str, http: requests.Session, two_accounts):
    """
    Regra de negócio:
    saldo insuficiente -> 400
    """
    from_id, to_id = two_accounts

    transfer = http.post(
        f"{base_url}/transfers",
        json={"from_account_id": from_id, "to_account_id": to_id, "amount": 999999.0},
        timeout=10,
    )

    assert transfer.status_code == 400
    assert "Insufficient balance" in transfer.text


def test_transfer_rejects_same_account(base_url: str, http: requests.Session, create_account):
    """
    Regra: origem e destino não podem ser a mesma conta -> 400
    """
    r = create_account("Same Account User", 50.0)
    assert r.status_code == 201
    acc_id = r.json()["id"]

    transfer = http.post(
        f"{base_url}/transfers",
        json={"from_account_id": acc_id, "to_account_id": acc_id, "amount": 10.0},
        timeout=10,
    )

    assert transfer.status_code == 400
    assert "must differ" in transfer.text


def test_transfer_not_found_account(base_url: str, http: requests.Session):
    """
    Conta inexistente -> 404
    """
    transfer = http.post(
        f"{base_url}/transfers",
        json={"from_account_id": 999999, "to_account_id": 1, "amount": 10.0},
        timeout=10,
    )
    assert transfer.status_code == 404