from sqlalchemy import String, Integer, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Account(Base):
    """
    Conta bancária simples para o nosso lab:
    - owner_name: dono da conta
    - balance: saldo
    """
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_name: Mapped[str] = mapped_column(String(120), nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0.0)


class Transfer(Base):
    """
    Transferência entre contas.
    """
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    from_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    to_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())