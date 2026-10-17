from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    development_jwt_secret: str = "development-only-change-this-secret-key"
    app_name: str = "IT seobiseu API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    frontend_origins: str = "http://localhost:5500,http://127.0.0.1:5500"
    oracle_user: str = ""
    oracle_password: str = ""
    oracle_dsn: str = ""
    oracle_wallet_dir: str = ""
    database_mode: str = "sqlite"
    sqlite_path: str = "it_seobiseu.db"
    seed_admin_email: str = "admin@it-seobiseu.local"
    seed_admin_password: str = "Admin123!"
    jwt_secret_key: str = Field(default=development_jwt_secret, min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.app_env.lower() != "production":
            return self
        if self.use_sqlite:
            raise ValueError("DATABASE_MODE debe ser oracle en producción.")
        if not all((self.oracle_user, self.oracle_password, self.oracle_dsn, self.oracle_wallet_dir)):
            raise ValueError("Oracle y ORACLE_WALLET_DIR son obligatorios en producción.")
        if self.jwt_secret_key == self.development_jwt_secret:
            raise ValueError("JWT_SECRET_KEY debe cambiarse en producción.")
        if not self.origins or any(origin.startswith("http://") for origin in self.origins):
            raise ValueError("FRONTEND_ORIGINS debe usar HTTPS en producción.")
        return self

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_origins.split(",") if origin.strip()]

    @property
    def use_sqlite(self) -> bool:
        return self.database_mode.lower() == "sqlite"


@lru_cache
def get_settings() -> Settings:
    return Settings()
