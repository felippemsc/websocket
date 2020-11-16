import aiohttp_cors

from aiohttp import web

from app.views import health_check
from app.views.ws_handler import websocket_handler, connection_handler


def create_app():
    app = web.Application()

    app.router.add_get('/health-check', health_check)
    app.router.add_get('/connection/{key}', connection_handler)
    app.add_routes([web.get('/websocket', websocket_handler)])

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    return app
