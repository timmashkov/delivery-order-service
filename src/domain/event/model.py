from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class EventStatusEnum(Enum):
    WAITING_FOR_SENDING = "WAITING_FOR_SENDING"
    SENT = "SENT"
    CREATED = "CREATED"
    UNSENT = "UNSENT"
    ARCHIVED = "ARCHIVED"


@dataclass
class EventDomainModel:
    event_type: str
    data: dict | None
    entity_id: UUID | None
    status: EventStatusEnum = EventStatusEnum.CREATED
    sent_at: datetime = datetime.now(timezone.utc)

    def __post_init__(self) -> None:
        self.uuid: UUID = uuid4()
        self.created_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
