from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import engine, Base, get_db
from app.db.models import Account, Transfer
from app.api.schemas import AccountCreate, AccountOut, TransferCreate, TransferOut


app = FastAPI(title="Quality Lab Fintech", version="0.1.0")


@app.on_event("startup")
def startup():
    """
    Para simplificar no início:
    - cria as tabelas automaticamente no startup.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    """
    Endpoint simples para healthcheck.
    
    """
    return {"status": "ok"}


@app.post("/accounts", response_model=AccountOut, status_code=201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    """
    Cria uma conta com saldo inicial.
    """
    account = Account(owner_name=payload.owner_name, balance=payload.initial_balance)
    db.add(account)
    db.commit()
    db.refresh(account)  # garante que o ID foi carregado após commit
    return account


@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: int, db: Session = Depends(get_db)):
    """
    Retorna saldo da conta.
    """
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return {"account_id": account.id, "balance": float(account.balance)}


@app.post("/transfers", response_model=TransferOut, status_code=201)
def create_transfer(payload: TransferCreate, db: Session = Depends(get_db)):
    """
    Executa transferência simples.
    Regras:
    - contas precisam existir
    - contas diferentes
    - saldo suficiente
    """
    if payload.from_account_id == payload.to_account_id:
        raise HTTPException(status_code=400, detail="from_account_id must differ from to_account_id")

    from_acc = db.get(Account, payload.from_account_id)
    to_acc = db.get(Account, payload.to_account_id)

    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if float(from_acc.balance) < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Debita e credita
    from_acc.balance = float(from_acc.balance) - payload.amount
    to_acc.balance = float(to_acc.balance) + payload.amount

    # Registra transferência
    transfer = Transfer(
        from_account_id=payload.from_account_id,
        to_account_id=payload.to_account_id,
        amount=payload.amount,
    )
    db.add(transfer)

    db.commit()
    db.refresh(transfer)

    return transfer