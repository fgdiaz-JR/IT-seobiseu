from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IT seobiseu API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    frontend_origins: str = "http://localhost:5500,http://127.0.0.1:5500"
    oracle_user: str = ""
    oracle_password: str = ""
    oracle_dsn: str = ""
    database_mode: str = "sqlite"
    sqlite_path: str = "it_seobiseu.db"
    seed_admin_email: str = "admin@it-seobiseu.local"
    seed_admin_password: str = "Admin123!"
    jwt_secret_key: str = Field(
        default="development-only-change-this-secret-key",
        min_length=32,
    )
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_origins.split(",") if origin.strip()]

    @property
    def use_sqlite(self) -> bool:
        return self.database_mode.lower() == "sqlite"


@lru_cache
def get_settings() -> Settings:
    return Settings()
