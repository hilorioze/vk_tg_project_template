from src.configurator.utils import get_config
import pytest
from pydantic.error_wrappers import ValidationError
from src.modules import json

null, false, true = None, False, True
JSON = '{"database": {"sql": {"host": "localhost", "port": 5432, "username": "postgres", "password": "postgres", "database": "postgres", "ssl_ca": null, "ssl_cert": null, "ssl_key": null, "debug": false, "isolation_level": "READ COMMITTED", "dialect": "postgres", "driver": "asyncpg", "url": "postgres://postgres:postgres@localhost:5432/postgres", "args": {}, "tables": {}}, "redis": {"host": "localhost", "port": 6379, "password": "", "database": 0, "ssl_ca_certs": null, "debug": false, "url": "redis://localhost:6379", "args": {}}}, "loop": {"aiomonitor": {"enabled": false, "host": "127.0.0.1", "port": 50101, "console_port": 50102, "console_enabled": true}, "debug": false, "uvloop": false}, "logging": {"level": "DEBUG", "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <5}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"}}'
DICT = {"database": {"sql": {"host": "localhost", "port": 5432, "username": "postgres", "password": "postgres", "database": "postgres", "ssl_ca": null, "ssl_cert": null, "ssl_key": null, "debug": false, "isolation_level": "READ COMMITTED", "dialect": "postgres", "driver": "asyncpg", "url": "postgres://postgres:postgres@localhost:5432/postgres", "args": {}, "tables": {}}, "redis": {"host": "localhost", "port": 6379, "password": "", "database": 0, "ssl_ca_certs": null, "debug": false, "url": "redis://localhost:6379", "args": {}}}, "loop": {"aiomonitor": {"enabled": false, "host": "127.0.0.1", "port": 50101, "console_port": 50102, "console_enabled": true}, "debug": false, "uvloop": false}, "logging": {"level": "DEBUG", "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <5}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"}}


def test_load():
    cfg = get_config(JSON)
    assert cfg.dict() == DICT

    with pytest.raises(ValidationError):
        get_config('{"something": 1234}')

    with pytest.raises(json.JSONDecodeError):
        get_config('something')

        