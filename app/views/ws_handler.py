import asyncio
import json

from datetime import datetime

from aiohttp import web

TIME_TO_UPDATE = 15
TIME_TO_CLOSE_WS = 1 * 30


async def websocket_handler(request):
    scheduled_tasks = []

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    def update_client():
        now = datetime.now().isoformat()
        asyncio.ensure_future(ws.send_str(f"Hello from Server at {now}!"))

    def close_connection():
        asyncio.ensure_future(ws.close(code=408, message=b"Timeout"))

    loop = asyncio.get_event_loop()

    for i in range(1, TIME_TO_CLOSE_WS // TIME_TO_UPDATE):
        scheduled_tasks.append(loop.call_later(i * TIME_TO_UPDATE, update_client))
    scheduled_tasks.append(loop.call_later(TIME_TO_CLOSE_WS, close_connection))

    async for msg in ws:
        content = json.loads(msg.data)
        if content["msg"] == "__ping__":
            await ws.send_str("__pong__")
        elif content["msg"] == "Hello from Client!":
            await ws.send_str("Hello from Server!")

    for scheduled_task in scheduled_tasks:
        scheduled_task.cancel()
    return ws
