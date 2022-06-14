from src.database.sql import setup_database
from src.runner._constants import TASKS as _TASKS

__all__ = (
    "STARTUP_TASKS",
    "SHUTDOWN_TASKS",
)

STARTUP_TASKS: _TASKS = [setup_database()]
SHUTDOWN_TASKS: _TASKS = []
