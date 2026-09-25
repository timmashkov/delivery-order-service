from datetime import datetime
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter

from domain import OrderDomainModel
from domain.event.model import EventDomainModel
from infrastructure.broker.kafka import KafkaProducer
from infrastructure.database import UnitOfWork, RepositoryMixin, Order, OutboxRepository


class OrderUseCase(RepositoryMixin):

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work
        self._model = Order

    async def get_orders_list(self, filters: Filter) -> list:
        async with self.read_repository() as read_repository:
            orders_list = await read_repository.get_all_objects(filters)
        return [order for order in orders_list]

    async def read_single_order(self, order_uuid: UUID):
        async with self.read_repository() as read_repository:
            result = await read_repository.get_object_by_uuid(order_uuid)
            return result

    @staticmethod
    def _prepare_domain_models(**kwargs) -> tuple[OrderDomainModel, EventDomainModel]:
        new_order_model = OrderDomainModel(**kwargs)
        new_event_model = EventDomainModel(
            event_type="create_order",
            data=new_order_model.to_json(),
            entity_id=new_order_model.uuid,
        )
        return new_order_model, new_event_model

    async def create_new_order(self, **kwargs):
        new_order_model, new_event_model = self._prepare_domain_models(**kwargs)
        async with self._unit_of_work as unit_of_work:
            outbox_repository = unit_of_work.repositories.custom_repository(OutboxRepository)
            order_repository = unit_of_work.repositories.write_repository(model=self._model)
            new_order = await order_repository.create_object(**new_order_model.to_dict())
            await outbox_repository.create_event(**new_event_model.to_dict())
        return new_order

    async def update_order(self, **kwargs):
        uuid = kwargs.pop("order_uuid")
        async with self.write_repository() as write_repository:
            return await write_repository.update_object(**kwargs, uuid=uuid)

    async def delete_order(self, order_uuid: UUID):
        async with self.write_repository() as write_repository:
            return await write_repository.delete_object(order_uuid)
