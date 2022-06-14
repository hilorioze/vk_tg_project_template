from vkbottle import BotPolling
from vkbottle.bot import Bot

from src import api
from src.blueprints import bps
from src.configurator import config
from src.custom import StateDispenser, bot_error_handler
from src.middlewares import mws
from src.modules import loop

__all__ = ("bot",)

polling = BotPolling(group_id=config.bot.group_id)
bot = Bot(
    api=api.api,
    polling=polling,
    state_dispenser=StateDispenser(),
    error_handler=bot_error_handler,
    loop=loop,
    task_each_event=True,
)

for mw in mws:
    bot.labeler.message_view.register_middleware(mw)

for bp in bps:
    bp.load(bot)
