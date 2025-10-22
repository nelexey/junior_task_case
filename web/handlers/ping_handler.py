from aiohttp import web
from asyncio import sleep

from ..middlewares import middleware, semaphore

@middleware(semaphore(10, 10))
async def ping_handler(request: web.Request) -> web.Response:
    return web.Response(text='OK')
