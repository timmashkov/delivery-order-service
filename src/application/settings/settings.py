from pathlib import Path

from pydantic import Field

from application.settings._app_config import AppSettings
from application.settings._broker_config import KafkaSettings
from application.settings._database_config import DatabaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict

_SETTINGS_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SETTINGS_DIR.parent.parent.parent  # order_service/


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)
