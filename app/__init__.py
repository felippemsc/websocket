from aiohttp import web

from app.views import health_check
from app.views.ws_handler import websocket_handler


def create_app():
    app = web.Application()

    app.router.add_get('/health-check', health_check)
    app.add_routes([web.get('/websocket', websocket_handler)])

    return app
