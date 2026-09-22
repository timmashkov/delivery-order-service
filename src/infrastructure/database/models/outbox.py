from datetime import datetime

from sqlalchemy import String, DateTime, UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column

from domain import EventStatusEnum
from infrastructure.database.models._base import _Base
from infrastructure.database.models._mixins import UUIDTableMixin, CreatedAtTableMixin


class Outbox(_Base, UUIDTableMixin, CreatedAtTableMixin):
    event_type: Mapped[str] = mapped_column(
        String,
        unique=False,
        index=True,
        comment="Тип события",
    )
    sent_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True, comment="Время отправки")
    entity_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="Уникальный айди сущности",
    )
    status: Mapped[EventStatusEnum] = mapped_column(
        Enum(EventStatusEnum, name='event_status_enum', create_type=False),
        nullable=False,
        default=EventStatusEnum.CREATED,
    )