import logging
import typing

import pydantic

__all__ = ("ConfigModel",)


class Redis(pydantic.BaseModel):
    host: str
    port: int
    password: typing.Optional[str] = None
    database: int
    ssl_ca_certs: typing.Optional[str] = None
    debug: bool
    url: typing.Optional[str] = None
    args: dict = {}

    @pydantic.root_validator(pre=True)
    def check_url(cls, values):
        """
        Construct the URL if it is not provided.
        """
        if values.get("url") is None:
            values["url"] = (
                f"redis://"
                f"{values['password']}@"
                f"{values['host']}:"
                f"{values['port']}/"
                f"{values['database']}"
            )
        return values


class Tables(pydantic.BaseModel):
    users: str
    states: str


class Sql(pydantic.BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str
    ssl_ca: typing.Optional[str] = None
    ssl_cert: typing.Optional[str] = None
    ssl_key: typing.Optional[str] = None
    debug: bool
    isolation_level: typing.Optional[str] = None
    dialect: str
    driver: str
    url: typing.Optional[str] = None
    args: dict = {}
    tables: Tables

    @pydantic.root_validator(pre=True)
    def check_url(cls, values):
        """
        Construct the URL if it is not provided.
        """
        if values["url"] is None:
            values["url"] = (
                f"{values['dialect']}+{values['driver']}://"
                f"{values['username']}:{values['password']}@"
                f"{values['host']}:{values['port']}/"
                f"{values['database']}"
            )
        return values


class Database(pydantic.BaseModel):
    sql: Sql
    redis: Redis


class Aiomonitor(pydantic.BaseModel):
    enabled: bool
    host: str
    port: int
    console_port: int
    console_enabled: bool


class Loop(pydantic.BaseModel):
    aiomonitor: Aiomonitor
    debug: bool
    uvloop: bool


class Logging(pydantic.BaseModel):
    level: typing.Union[str, int]
    format: str

    @pydantic.validator("level")
    def check_level(cls, level):
        """
        Convert the level to an integer.
        """
        if isinstance(level, str):
            _levels = list(logging._nameToLevel.keys())  # noqa
            if level.upper() not in _levels:
                raise ValueError(
                    f"Invalid log level: {level}\n" f"Valid levels: {', '.join(_levels)}"  # noqa
                )
        return level


class Bot(pydantic.BaseModel):
    token: typing.Union[str, typing.List[str]]
    group_id: typing.Optional[int]
    proxy: typing.Optional[str]


class ConfigModel(pydantic.BaseModel):
    bot: Bot
    database: Database
    loop: Loop
    logging: Logging
