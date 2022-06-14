import signal
import sys
import typing
from functools import partial

TASKS = typing.List[typing.Union[typing.Awaitable, partial]]
win32 = sys.platform == "win32"
signals = (
    (
        signal.SIGBREAK,  # type: ignore
        signal.CTRL_C_EVENT,  # type: ignore
    )
    if win32
    else (
        signal.SIGINT,
        signal.SIGTERM,
    )
)
