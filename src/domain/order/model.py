from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder


class OrderStatusEnum(StrEnum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class CurrencyEnum(StrEnum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"
    JPY = "JPY"


@dataclass
class OrderDomainModel:
    user_uuid: UUID

    status: OrderStatusEnum

    total_amount: Decimal

    currency: CurrencyEnum

    def __post_init__(self) -> None:
        self.uuid: UUID = uuid4()
        self.created_at = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        base_dict = asdict(self)
        base_dict["user_uuid"] = str(self.user_uuid)
        base_dict["uuid"] = str(self.uuid)
        base_dict["created_at"] = self.created_at
        return base_dict

    def to_json(self) -> dict[str, Any]:
        return jsonable_encoder(asdict(self))
