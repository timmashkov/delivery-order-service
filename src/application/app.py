from presentation.routers import perm_router, role_router, user_router

from .server import APIServer

service_app = APIServer(
    name="service_app",
    routers=[user_router, perm_router, role_router],
).app
