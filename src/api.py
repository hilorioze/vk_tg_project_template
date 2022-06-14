import ssl

import certifi
from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector
from vkbottle import SingleAiohttpClient
from vkbottle.api import API

from src.configurator import config

__all__ = (
    "api",
    "set_custom_http_client",
)

api = API(token=config.bot.token)


async def set_custom_http_client(*apis: API) -> None:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = (
        ProxyConnector.from_url(url=config.bot.proxy, ssl_context=ssl_context)
        if config.bot.proxy
        else TCPConnector(ssl_context=ssl_context)
    )
    session = ClientSession(connector=connector)
    http_client = SingleAiohttpClient(session=session)
    for _api in apis:
        _api.http_client = http_client
