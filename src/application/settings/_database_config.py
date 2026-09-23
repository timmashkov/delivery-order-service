from pydantic import Field

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    dialect: str = "postgresql"
    host: str
    port: int
    login: str
    password: str
    database: str
    pool_min_size: int = Field(default=5)
    pool_max_size: int = Field(default=10)
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False
