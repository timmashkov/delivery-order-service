from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from domain import OrderStatusEnum
from infrastructure.database.models import Order
from presentation.models.patched_filter import PatchedFilter


class CreateOrderModel(BaseModel):
    user_uuid: UUID
    status: OrderStatusEnum
    total_amount: Decimal
    currency: str


class ReadOrderModel(CreateOrderModel):
    uuid: UUID = Field(description=Order.uuid.comment)
    created_at: datetime = Field(description=Order.created_at.comment)
    updated_at: datetime = Field(description=Order.updated_at.comment)


class OrderFilter(PatchedFilter):
    uuid: UUID | None = None
    user_uuid: UUID | None = None
    status: OrderStatusEnum | None = None
    currency: str | None = None

    class Constants(PatchedFilter.Constants):
        model = Order
