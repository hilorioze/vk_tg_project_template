import asyncio
from functools import partial

import aiomonitor

from src.configurator import config
from src.modules import logger, loop
from src.runner._constants import signals
from src.runner.tasks import SHUTDOWN_TASKS, STARTUP_TASKS

__all__ = ("run",)


def _raise_graceful_exit() -> None:
    raise SystemExit(1)


async def _wakeup():
    while True:
        await asyncio.sleep(3600)


def run():
    """
    Run the application.
    :return:
    """
    STARTUP_TASKS.append(_wakeup())
    from src.runner import shutdown

    if config.loop.aiomonitor.enabled:
        monitor = aiomonitor.Monitor(
            loop=loop,
            host=config.loop.aiomonitor.host,
            port=config.loop.aiomonitor.port,
            console_port=config.loop.aiomonitor.console_port,
            console_enabled=config.loop.aiomonitor.console_enabled,
            locals=globals(),
        )
        STARTUP_TASKS.append(partial(monitor.start))
        SHUTDOWN_TASKS.append(partial(monitor.close))

    try:
        for sig in signals:
            loop.add_signal_handler(sig, shutdown.stop)
    except NotImplementedError:
        pass

    for startup_task in STARTUP_TASKS:
        logger.info("Execute task on startup {}", startup_task)
        if asyncio.iscoroutine(startup_task) or asyncio.isfuture(startup_task):
            loop.create_task(startup_task)
        elif callable(startup_task):
            loop.run_until_complete(loop.run_in_executor(None, startup_task))
        else:
            raise TypeError(f"Task {startup_task} must be a coroutine or a callable.")

    try:
        loop.run_forever()
    except (SystemExit, KeyboardInterrupt):
        pass
    finally:
        shutdown.stop()


if __name__ == "__main__":
    run()
