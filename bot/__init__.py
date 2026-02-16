import asyncio
import os

from bot.log import setup_logger


setup_logger()


if os.name != "nt":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy()) # ty: ignore[deprecated]
