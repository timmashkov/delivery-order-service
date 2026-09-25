from pydantic import Field

from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    host: str
    port: int
    transactional_id: str
    acks: str = "all"
    topics: list[str] = Field(default_factory=list)
