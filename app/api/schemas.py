from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    """
    Payload para criar conta.
    """
    owner_name: str = Field(min_length=2, max_length=120)
    initial_balance: float = Field(default=0.0, ge=0.0)


class AccountOut(BaseModel):
    """
    Resposta ao criar/consultar conta.
    """
    id: int
    owner_name: str
    balance: float

    class Config:
        from_attributes = True  # permite ler direto de objetos ORM


class TransferCreate(BaseModel):
    """
    Payload de transferência.
    """
    from_account_id: int = Field(gt=0)
    to_account_id: int = Field(gt=0)
    amount: float = Field(gt=0.0)


class TransferOut(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount: float

    class Config:
        from_attributes = True