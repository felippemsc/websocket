import asyncio
import json
import uuid

from collections import namedtuple

import redis

from aiohttp import web

from app.utils import create_user_code, WebSocketTalker as talker

Integration = namedtuple('Integration', ['user_code', 'websocket', 'token'])

TIME_TO_UPDATE = 30
TIME_TO_CLOSE_WS = 2 * 60

INTEGRATION_KEYS = dict()


async def websocket_handler(request):
    scheduled_tasks = []
    curr_id_key = str(uuid.uuid4())

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    def update_code():
        nonlocal curr_id_key
        new_id_key = str(uuid.uuid4())
        INTEGRATION_KEYS[new_id_key] = INTEGRATION_KEYS[curr_id_key]
        asyncio.ensure_future(
            ws.send_str(
                talker.send_code(msg=f"Sending a new Identification Key: {new_id_key}!", key=new_id_key)
            )
        )
        INTEGRATION_KEYS.pop(curr_id_key)
        curr_id_key = new_id_key

    def close_connection():
        asyncio.ensure_future(ws.send_str(talker.timeout()))
        asyncio.ensure_future(ws.close())

    loop = asyncio.get_event_loop()

    for i in range(1, TIME_TO_CLOSE_WS // TIME_TO_UPDATE):
        scheduled_tasks.append(loop.call_later(i * TIME_TO_UPDATE, update_code))
    scheduled_tasks.append(loop.call_later(TIME_TO_CLOSE_WS, close_connection))

    async for msg in ws:
        content = json.loads(msg.data)
        if content["msg"] == "__ping__":
            await ws.send_str(talker.pong())
        elif content["msg"] == "Hey! Here is a Token":
            INTEGRATION_KEYS[curr_id_key] = Integration(
                user_code=create_user_code(),
                websocket=ws,
                token=content["token"]
            )
            await ws.send_str(
                talker.send_code(
                    msg=f"Thank's for the token! Here is a Identification Key: {curr_id_key}", key=curr_id_key
                )
            )

    for scheduled_task in scheduled_tasks:
        scheduled_task.cancel()
    INTEGRATION_KEYS.pop(curr_id_key)
    return ws


async def connection_handler(request):
    key = request.match_info['key']
    integration = INTEGRATION_KEYS.get(key, None)
    if integration is not None:
        await integration.websocket.send_str(talker.success())
        await integration.websocket.close()

        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set(integration.token, integration.user_code, ex=30 * 60)
        return web.json_response({"secret": integration.user_code})

    raise web.HTTPNotFound()
