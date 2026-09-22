import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4


@dataclass
class ProductDomainModel:
    category_uuid: UUID
    name: str
    description: str | None
    price: Decimal
    currency: str
    is_active: bool
    data: dict | None

    def __post_init__(self) -> None:
        self.uuid: UUID = uuid4()
        self.created_at = datetime.now()
        self.sku = self._generate_sku(self.uuid, self.created_at)

    def to_dict(self) -> dict[str, Any]:
        base_dict = asdict(self)
        base_dict["uuid"] = self.uuid
        base_dict["created_at"] = self.created_at
        base_dict["sku"] = self.sku
        return base_dict

    def _generate_sku(self, uuid: UUID, creation_date: datetime) -> str:
        vowels = re.findall(r'[aeiouAEIOU]', self.name)
        product_uuid = str(uuid).split("-")[-1]
        product_dat = creation_date.date().isoformat().replace("-", "").replace("0", "")[::-1]
        return product_uuid + "".join(vowels) + product_dat
