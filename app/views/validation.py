import redis
import pyotp

from aiohttp import web


async def validation_handler(request):
    body = await request.json()
    r = redis.Redis(host='localhost', port=6379, db=0)
    secret = r.get(body['token'])
    totp = pyotp.TOTP(secret.decode('utf-8'))
    if totp.verify(body['code']):
        return web.json_response({"result": "ok"})

    raise web.HTTPBadRequest()
