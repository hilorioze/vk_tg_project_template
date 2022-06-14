from importlib import reload

from src._modules import get_json
from src.configurator.model import ConfigModel

__all__ = (
    "get_config",
    "reload_config",
)


def reload_config():
    """
    Reload the config
    """
    from src import configurator

    reload(module=configurator)


def get_config(json_string: str) -> ConfigModel:
    """
    Get config from the json string
    :param json_string: json string
    :return: ConfigModel
    """
    _config = get_json().loads(json_string)
    return ConfigModel(**_config)
