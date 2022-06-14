from vkbottle.bot import Blueprint, Message

from src.database.models import User
from src.rules import UserRegisteredRule

__all__ = ("bp",)


bp = Blueprint(__name__)


@bp.on.private_message(UserRegisteredRule())
async def profile_handler(m: Message, user: User):
    await m.answer(f"Your Profile:\nID: {user.id}\nCreated: {user.created_at}")
