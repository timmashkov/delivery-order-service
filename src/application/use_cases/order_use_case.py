from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter

from infrastructure.database import UnitOfWork, RepositoryMixin, Order


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

    async def create_new_order(self, **kwargs):
        async with self.write_repository() as write_repository:
            return await write_repository.create_object(**kwargs)

    async def update_order(self, **kwargs):
        uuid = kwargs.pop("order_uuid")
        async with self.write_repository() as write_repository:
            return await write_repository.update_object(**kwargs, uuid=uuid)

    async def delete_order(self, order_uuid: UUID):
        async with self.write_repository() as write_repository:
            return await write_repository.delete_object(order_uuid)
