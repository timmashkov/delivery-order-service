from pydantic import Field

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    name: str
    host: str
    port: int
    log_level: str
