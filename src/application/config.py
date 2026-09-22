from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    name: str
    host: str
    port: int
    log_level: str

    # PostgreSQL
    postgres_dialect: str
    postgres_host: str
    postgres_port: int
    postgres_login: str
    postgres_password: str
    postgres_database: str
    postgres_pgbouncer: bool
    postgres_echo: bool
    postgres_pool_min_size: int
    postgres_pool_max_size: int
    postgres_pool_timeout: int
    postgres_mat_view_time: int
