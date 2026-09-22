from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, UUID, Enum, Integer, ForeignKey, DECIMAL, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models._base import _Base
from infrastructure.database.models._mixins import UUIDTableMixin, CreatedAtTableMixin, UpdatedAtTableMixin

if TYPE_CHECKING:
    from .order import Order


class OrderItem(_Base, UUIDTableMixin):
    order_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("orders.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Идентификатор заказа",
    )

    product_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="Идентификатор продукта",
    )

    product_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Название продукта на момент заказа",
    )

    sku: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="SKU продукта на момент заказа",
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        comment="Цена одной единицы на момент заказа",
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Количество",
    )

    total_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        comment="Стоимость позиции",
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )
