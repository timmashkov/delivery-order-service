from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from infrastructure.database.models import OrderItem
from presentation.models.patched_filter import PatchedFilter


class CreateOrderItemModel(BaseModel):
    order_uuid: UUID
    product_uuid: UUID
    product_name: str
    unit_price: Decimal
    sku: str
    quantity: int
    total_price: Decimal


class ReadOrderItemModel(CreateOrderItemModel):
    uuid: UUID = Field(description=OrderItem.uuid.comment)
    created_at: datetime = Field(description=OrderItem.created_at.comment)
    updated_at: datetime = Field(description=OrderItem.updated_at.comment)


class OrderItemFilter(PatchedFilter):
    uuid: UUID | None = None
    order_uuid: UUID | None = None
    product_uuid: UUID | None = None
    currency: str | None = None

    class Constants(PatchedFilter.Constants):
        model = OrderItem
