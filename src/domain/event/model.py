from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class EventStatusEnum(Enum):
    PROCESSING = "PROCESSING"
    SENT = "SENT"
    CREATED = "CREATED"
    UNSENT = "UNSENT"
    ARCHIVED = "ARCHIVED"


@dataclass
class EventDomainModel:
    event_type: str
    data: dict | None
    entity_id: UUID
    status: EventStatusEnum = EventStatusEnum.CREATED
    sent_at: datetime = datetime.now()

    def __post_init__(self) -> None:
        self.uuid: UUID = uuid4()
        self.created_at = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        base_dict = asdict(self)
        base_dict["uuid"] = str(self.uuid)
        base_dict["created_at"] = self.created_at
        base_dict["entity_id"] = str(self.entity_id)
        return base_dict
