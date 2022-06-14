from __future__ import annotations

import asyncio
import sys
from importlib import import_module
from importlib.util import find_spec

from choicelib import choice_in_order
from typing_extensions import Protocol

__all__ = (
    "get_loop",
    "get_json",
    "get_logger",
    "JSONModule",
)


class JSONModule(Protocol):
    def loads(self, s: str) -> dict:
        ...

    def dumps(self, o: dict) -> str:
        ...


def get_loop():
    """
    Get asyncio loop.
    :return:
    """
    from src.configurator import config

    loop: asyncio.AbstractEventLoop

    if config.loop.uvloop:
        if find_spec("uvloop"):
            asyncio.set_event_loop_policy(import_module("uvloop").EventLoopPolicy())
        else:
            get_logger().warning("uvloop not found, falling back to default loop")

    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().new_event_loop()

    loop.set_debug(config.loop.debug)

    asyncio.set_event_loop(loop)
    return loop


def get_logger():
    """
    Get logger.
    :return:
    """

    from src.configurator import config

    try:
        import loguru
    except ImportError:
        raise ImportError("loguru not found, please install it.")
    logger = loguru.logger
    logger.remove()
    logger.add(
        sink=sys.stdout,
        level=config.logging.level,
        format=config.logging.format,
        colorize=True,
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )
    return logger


def get_json():
    """
    Get json module.
    :return:
    """

    json: JSONModule = choice_in_order(
        ["ujson", "hyperjson", "orjson"], do_import=True, default="json"
    )
    return json
