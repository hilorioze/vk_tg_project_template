import asyncio
from alembic import context

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.configurator import config
from src.database.sql import engine, Base

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=config.database.sql.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():

    async with engine.connect() as conn:
        await conn.run_sync(do_run_migrations)

    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
