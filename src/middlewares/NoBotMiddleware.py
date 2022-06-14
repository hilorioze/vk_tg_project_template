from vkbottle import BaseMiddleware
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

__all__ = ("NoBotMiddleware",)


class NoBotMiddleware(BaseMiddleware[BaseMessageMin]):
    """
    Middleware that checks if the sender is a bot
    """

    async def pre(self) -> None:
        if self.event.from_id < 0:
            self.stop("Sender is a bot.")
