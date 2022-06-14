# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.configurator import config
from src.modules import json

__all__ = (
    "engine",
    "Base",
    "setup_database",
)

engine: AsyncEngine = create_async_engine(
    url=config.database.sql.url,
    echo=config.database.sql.debug,
    isolation_level=config.database.sql.isolation_level,
    json_serializer=json.dumps,
    json_deserializer=json.loads,
    **config.database.sql.args,
)
Base = declarative_base(bind=engine)  # noqa


async def setup_database():
    """
    Set up the database.
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
