import uuid
from datetime import datetime

from sqlalchemy import UUID, func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDTableMixin:
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Уникальный айди записи",
    )


class CreatedAtTableMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now(), comment="Дата создания"
    )


class UpdatedAtTableMixin:
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(),
        onupdate=datetime.now(),
        comment="Дата обновления",
    )
