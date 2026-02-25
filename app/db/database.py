from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.api.settings import settings


class Base(DeclarativeBase):
    """
    Base declarativa do SQLAlchemy (2.x).
    Todas as tabelas vão herdar daqui.
    """
    pass


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # evita conexões quebradas
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db():
    """
    Dependency do FastAPI.
    Abre uma sessão por request e garante fechamento.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()