from aiohttp import web

from app.views import health_check


def create_app():
    app = web.Application()

    app.router.add_get('/health-check', health_check)

    return app
