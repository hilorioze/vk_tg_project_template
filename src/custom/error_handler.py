from vkbottle import ErrorHandler

from src.modules import logger

bot_error_handler = ErrorHandler(redirect_arguments=True)


async def bot_error_handler_undefined_error(error: Exception, *args, **kwargs) -> None:
    logger.exception(f"Undefined error: {error}\nargs: {args}\nkwargs: {kwargs}")


bot_error_handler.register_undefined_error_handler(bot_error_handler_undefined_error)
