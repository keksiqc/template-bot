from __future__ import annotations

import asyncio
import os

from bot.log import init_logging


init_logging()


if os.name != "nt":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # ty: ignore[deprecated]
