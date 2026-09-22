from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter

from infrastructure.database import UnitOfWork, RepositoryMixin, OrderItem


class OrderItemUseCase(RepositoryMixin):

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work
        self._model = OrderItem

    async def get_order_items_list(self, filters: Filter) -> list:
        async with self.read_repository() as read_repository:
            order_items_list = await read_repository.get_all_objects(filters)
        return [order_item for order_item in order_items_list]

    async def read_single_order_item(self, order_item_uuid: UUID):
        async with self.read_repository() as read_repository:
            result = await read_repository.get_object_by_uuid(order_item_uuid)
            return result

    async def create_new_order_item(self, **kwargs):
        async with self.write_repository() as write_repository:
            return await write_repository.create_object(**kwargs)

    async def update_order_item(self, **kwargs):
        uuid = kwargs.pop("item_uuid")
        async with self.write_repository() as write_repository:
            return await write_repository.update_object(**kwargs, uuid=uuid)

    async def delete_order_item(self, order_item_uuid: UUID):
        async with self.write_repository() as write_repository:
            return await write_repository.delete_object(order_item_uuid)
