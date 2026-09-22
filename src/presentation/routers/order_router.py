from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi_filter import FilterDepends

from application.use_cases import OrderUseCase
from presentation.models import CreateOrderModel, ReadOrderModel, OrderFilter

order_router = APIRouter(prefix="/order", tags=["Orders"])


@order_router.get("/{order_uuid}", response_model=ReadOrderModel)
@inject
async def read_order(order_uuid: UUID, order_provider: FromDishka[OrderUseCase]):
    return await order_provider.read_single_order(order_uuid)


@order_router.get("/", response_model=list[ReadOrderModel])
@inject
async def read_orders(
    order_provider: FromDishka[OrderUseCase],
    order_filters: OrderFilter = FilterDepends(OrderFilter),
):
    return await order_provider.get_orders_list(order_filters)


@order_router.post("/", response_model=ReadOrderModel)
@inject
async def create_order(
    order_data: CreateOrderModel, order_provider: FromDishka[OrderUseCase]
):
    return await order_provider.create_new_order(**order_data.model_dump())


@order_router.patch("/{order_uuid}", response_model=ReadOrderModel)
@inject
async def update_order(
    order_uuid: UUID, order_data: CreateOrderModel, order_provider: FromDishka[OrderUseCase]
):
    return await order_provider.update_order( **order_data.model_dump(), product_uuid=order_uuid)


@order_router.delete("/{order_uuid}", response_model=ReadOrderModel)
@inject
async def delete_order(order_uuid: UUID, order_provider: FromDishka[OrderUseCase]):
    return await order_provider.delete_order(order_uuid)
