import pytest
from vkbottle.bot import Message
from src.middlewares import NoBotMiddleware
from vkbottle import MiddlewareError

event_ok = Message(
    **{'date': 1, 'from_id': 1, 'id': 1, 'out': 0, 'attachments': [], 'conversation_message_id': 1, 'fwd_messages': [],
       'important': False, 'is_hidden': False, 'peer_id': 1, 'random_id': 0, 'text': '123'})
event_no_ok = Message(
    **{'date': 1, 'from_id': -1, 'id': 1, 'out': 0, 'attachments': [], 'conversation_message_id': 1, 'fwd_messages': [],
       'important': False, 'is_hidden': False, 'peer_id': 1, 'random_id': 0, 'text': '123'})


@pytest.mark.asyncio
async def test_no_bot_middleware():
    no_bot_middleware_ok = NoBotMiddleware(event=event_ok)
    await no_bot_middleware_ok.pre()
    assert no_bot_middleware_ok.error is None
    no_bot_middleware_no_ok = NoBotMiddleware(event=event_no_ok)
    await no_bot_middleware_no_ok.pre()
    assert no_bot_middleware_no_ok.error.__str__() == "Sender is a bot."


