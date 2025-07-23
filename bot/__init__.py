from bot.log import setup_logger
import os
import asyncio

setup_logger()


if os.name != "nt":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())