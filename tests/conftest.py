import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Base URL da API.
    Boas práticas:
    - Centraliza a URL em 1 lugar
    - Facilita trocar para CI/staging no futuro
    """
    return BASE_URL


@pytest.fixture(scope="session")
def http() -> requests.Session:
    """
    Reutiliza conexões HTTP
    """
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
def create_account(base_url: str, http: requests.Session):
    """
    Fixture helper para criar contas.
    Retorna a response para o teste decidir asserções.
    """
    def _create(owner_name: str, initial_balance: float = 0.0) -> requests.Response:
        return http.post(
            f"{base_url}/accounts",
            json={
                "owner_name": owner_name,
                "initial_balance": initial_balance,
            },
            timeout=10,
        )

    return _create


def _extract_id(response: requests.Response) -> int:
    """
    Helper interno: extrai 'id' do JSON com validação mínima.
    """
    payload = response.json()
    if "id" not in payload:
        raise AssertionError(f"Resposta sem 'id': {payload}")
    return int(payload["id"])


@pytest.fixture
def two_accounts(create_account):
    """
    Cria duas contas para cenários de transferência.
    Retorna (from_id, to_id).
    """
    r1 = create_account("From User", 100.0)
    assert r1.status_code == 201, f"Falha ao criar conta origem: {r1.text}"
    from_id = _extract_id(r1)

    r2 = create_account("To User", 10.0)
    assert r2.status_code == 201, f"Falha ao criar conta destino: {r2.text}"
    to_id = _extract_id(r2)

    return from_id, to_id