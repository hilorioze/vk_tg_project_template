import asyncio

from src.modules import logger, loop
from src.runner._constants import signals
from src.runner.tasks import SHUTDOWN_TASKS

__all__ = ("stop",)


def stop():
    """
    Stop the application.
    :return:
    """
    try:
        for sig in signals:
            loop.remove_signal_handler(sig)
    except NotImplementedError:
        pass
    else:
        logger.info("Signal handlers has been removed")

    for shutdown_task in SHUTDOWN_TASKS:
        logger.info("Execute task on shutdown {}", shutdown_task)
        if asyncio.iscoroutine(shutdown_task) or asyncio.isfuture(shutdown_task):
            loop.run_until_complete(shutdown_task)
        elif callable(shutdown_task):
            loop.run_until_complete(loop.run_in_executor(None, shutdown_task))
        else:
            raise TypeError(f"Task {shutdown_task} must be a coroutine or a callable.")

    tasks_to_cancel = asyncio.all_tasks(loop=loop)
    if tasks_to_cancel:
        logger.info("Cancelling {} tasks", len(tasks_to_cancel))
        for task_to_cancel in tasks_to_cancel:
            logger.info("Cancelling task {}", task_to_cancel)
            task_to_cancel.cancel()

        loop.run_until_complete(asyncio.gather(*tasks_to_cancel, return_exceptions=True))

        for task_to_cancel in tasks_to_cancel:
            if task_to_cancel.cancelled():
                logger.info("Task {} has been cancelled", task_to_cancel)
                continue
            if task_to_cancel.exception() is not None:
                loop.call_exception_handler(
                    {
                        "message": "unhandled exception during asyncio.run() shutdown",
                        "exception": task_to_cancel.exception(),
                        "task": task_to_cancel,
                    }
                )
    logger.info("Shutdown all async generators")
    loop.run_until_complete(loop.shutdown_asyncgens())
