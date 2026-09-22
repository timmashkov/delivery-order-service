from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi_filter import FilterDepends

from application.use_cases import OrderItemUseCase
from presentation.models import ReadOrderItemModel, CreateOrderItemModel, OrderItemFilter

order_item_router = APIRouter(prefix="/item", tags=["OrderItems"])


@order_item_router.get("/{item_uuid}", response_model=ReadOrderItemModel)
@inject
async def read_order_item(item_uuid: UUID, order_item_provider: FromDishka[OrderItemUseCase]):
    return await order_item_provider.read_single_order_item(item_uuid)


@order_item_router.get("/", response_model=list[ReadOrderItemModel])
@inject
async def read_order_items(
    order_item_provider: FromDishka[OrderItemUseCase],
    order_item_filters: OrderItemFilter = FilterDepends(OrderItemFilter),
):
    return await order_item_provider.get_order_items_list(order_item_filters)


@order_item_router.post("/", response_model=ReadOrderItemModel)
@inject
async def create_order_item(
    order_item_data: CreateOrderItemModel, order_item_provider: FromDishka[OrderItemUseCase]
):
    return await order_item_provider.create_new_order_item(**order_item_data.model_dump())


@order_item_router.patch("/{item_uuid}", response_model=ReadOrderItemModel)
@inject
async def update_order_item(
    item_uuid: UUID, order_item_data: CreateOrderItemModel, order_item_provider: FromDishka[OrderItemUseCase]
):
    return await order_item_provider.update_order_item( **order_item_data.model_dump(), item_uuid=item_uuid)


@order_item_router.delete("/{item_uuid}", response_model=ReadOrderItemModel)
@inject
async def delete_order_item(item_uuid: UUID, order_item_provider: FromDishka[OrderItemUseCase]):
    return await order_item_provider.delete_order_item(item_uuid)
