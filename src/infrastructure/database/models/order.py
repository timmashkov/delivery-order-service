from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, UUID, Enum, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain import OrderStatusEnum
from infrastructure.database.models._base import _Base
from infrastructure.database.models._mixins import UUIDTableMixin, CreatedAtTableMixin, UpdatedAtTableMixin

if TYPE_CHECKING:
    from .order_item import OrderItem


class Order(_Base, UUIDTableMixin, CreatedAtTableMixin, UpdatedAtTableMixin):
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="Идентификатор пользователя",
    )

    status: Mapped[OrderStatusEnum] = mapped_column(
        Enum(OrderStatusEnum, name="order_status_enum"),
        nullable=False,
        default=OrderStatusEnum.CREATED,
        comment="Статус заказа",
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        comment="Общая стоимость заказа",
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="Валюта заказа",
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )
