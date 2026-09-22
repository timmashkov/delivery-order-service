import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Self

import uvicorn
from dishka import AsyncContainer
from dishka.integrations.fastapi import inject, setup_dishka
from fastapi import APIRouter, FastAPI, Request
from starlette.responses import JSONResponse

from application.config import Settings
from application.providers import ProvidersManager


class APIServer:
    @inject
    def __init__(
        self,
        settings: Settings,
        routers: list[APIRouter] | None = None,
        start_callbacks: list[Callable] | None = None,
        stop_callbacks: list[Callable] | None = None,
    ) -> None:
        self.container: AsyncContainer | None = None
        self._settings = settings
        self._app: FastAPI | None = None
        self._host = self._settings.host
        self._port = self._settings.port
        self._routers = routers or []
        self._start_callbacks = start_callbacks or []
        self._stop_callbacks = stop_callbacks or []

    def _init_server(self):
        self._app = FastAPI(title=self._settings.name, lifespan=self._lifespan)
        logging.basicConfig(
            level=self._settings.log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self._register_exception_handlers()
        self._init_routers()

    def _init_routers(self) -> None:
        for router in self._routers:
            self._app.include_router(router)
        logging.info("Routers init successfully!")

    @asynccontextmanager
    async def _lifespan(self, _app: FastAPI) -> AsyncGenerator:
        for callback in self._start_callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback()
            else:
                await asyncio.to_thread(callback)
        logging.info("Startup callbacks init successfully!")

        yield

        for callback in self._stop_callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback()
            else:
                await asyncio.to_thread(callback)
        logging.info("Shutdown callbacks init successfully!")

    def _register_exception_handlers(self) -> None:
        @self._app.exception_handler(Exception)
        async def general_error_handler(request: Request, exc: Exception):
            logging.error(f"Unhandled exception: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={type(exc).__name__: exc.__str__()},
            )

    @classmethod
    async def _create_server(cls) -> Self:
        container = ProvidersManager().make_container()
        server = await container.get(APIServer)
        server.container = container
        server._init_server()
        setup_dishka(app=server._app, container=container)
        return server

    @classmethod
    def run_server(cls) -> None:
        server = asyncio.run(cls._create_server())

        uvicorn.run(
            server._app,
            host=server._host,
            port=server._port,
        )
