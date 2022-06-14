from src.middlewares.NoBotMiddleware import NoBotMiddleware

__all__ = (
    "NoBotMiddleware",
    "mws",
)

mws = (NoBotMiddleware,)
