from src import api
from src.api import set_custom_http_client
from src.bot import bot
from src.database.sql import setup_database
from src.runner._constants import TASKS as _TASKS

__all__ = (
    "STARTUP_TASKS",
    "SHUTDOWN_TASKS",
)

STARTUP_TASKS: _TASKS = [
    setup_database(),
    set_custom_http_client(api.api),
    bot.run_polling(),
]
SHUTDOWN_TASKS: _TASKS = []
