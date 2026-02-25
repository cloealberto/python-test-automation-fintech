from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centraliza configurações do app.
    O Pydantic Settings é uma maneira fácil de lidar com configurações, especialmente quando queremos usar variáveis de ambiente.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # URL do banco (vamos usar Postgres via Docker)
    DATABASE_URL: str


settings = Settings()