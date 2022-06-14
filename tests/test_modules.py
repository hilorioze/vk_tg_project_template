import importlib

from src import modules, _modules
import logging
import asyncio

JSON_DATA = (
    {"a": 1, "b": "2", '3': 'c'},
    '{"a": 1, "b": "2", "3": "c"}',
)


def test_json():
    assert (modules.json is _modules.JSONModule) or (hasattr(modules.json, 'loads') is True and
                                                     hasattr(modules.json, 'dumps') is True)
    _1, _2 = modules.json.dumps(JSON_DATA[0]), modules.json.loads(JSON_DATA[1])
    assert _1.decode() if isinstance(_1, bytes) else _1 == JSON_DATA[1]
    assert modules.json.loads(JSON_DATA[1]) == JSON_DATA[0]


def test_logging():
    assert modules.logger is logging.Logger or importlib.import_module('loguru')._logger.Logger


def test_loop():
    assert issubclass(type(modules.loop), asyncio.AbstractEventLoop) is True
