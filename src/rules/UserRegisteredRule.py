import typing

from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from src.custom.error_handler import bot_error_handler
from src.database.repositories import UserRepository

__all__ = ("UserRegisteredRule",)


class UserRegisteredRule(ABCRule[BaseMessageMin]):
    """
    This rule checks if the user is registered in the database.
    If not, the function registers the user.
    """

    async def check(self, event: BaseMessageMin) -> typing.Union[bool, dict]:
        user_repository = UserRepository(event.from_id)
        user = await user_repository.get_user()
        if user is None:
            _user_registered = await user_repository.register(id=event.from_id)
            user_registered, exc = _user_registered[0], _user_registered[1]
            if not user_registered and exc:
                await bot_error_handler.handle(
                    exc, user=user, user_registered=user_registered, event=event
                )
                await event.answer("[#98] An error has occurred. Please, try again later.")
                return False
            else:
                user = await user_repository.get_user()
                if not user:
                    await event.answer("[#99] An error has occurred. Please, try again later.")
                    return False
                await event.answer("You have successfully registered.")
                return {"user": user, "user_repository": user_repository}
        else:
            return {"user": user, "user_repository": user_repository}
