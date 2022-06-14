from src._modules import get_json, get_logger, get_loop

json = get_json()
logger = get_logger()
loop = get_loop()

__all__ = ("json", "logger", "loop")
