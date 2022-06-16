import os
import re
from importlib import reload

from src._modules import get_json
from src.configurator.model import ConfigModel

__all__ = (
    "get_config",
    "reload_config",
)

# regex for environment variables
_ENV_REGEX = re.compile(r"\"\$\{(?P<env_var_name>\w+)(?P<type>\:\w+)?\}\"")  # type: ignore


def reload_config():
    """
    Reload the config
    """
    from src import configurator

    reload(module=configurator)


def replace_with_values_from_environment_variables(json_string: str) -> str:
    """
    Replace all the environment variables with their values in the json string
    Syntax:
    type is optional, if not specified, it will be string
    "${env_var_name:str}" -> str(env_var_value)
    "${env_var_name}" -> str(env_var_value)
    "${env_var_name:int}" -> int(env_var_value)
    "${env_var_name:float}" -> float(env_var_value)
    "${env_var_name:bool}" -> bool(env_var_value)
    "${env_var_name:list}" -> list(env_var_value)
    :param json_string: json string
    :return: json string with replaced values
    """
    from src._modules import get_json

    json_module = get_json()
    for match in _ENV_REGEX.finditer(json_string):
        env_var_name = match.group("env_var_name")
        env_var_type = match.group("type")
        env_var_value = os.environ.get(env_var_name)
        if env_var_value is None:
            raise ValueError(f'Environment variable "{env_var_name}" is not set')
        if env_var_type is None or env_var_type == ":str":
            json_string = json_string.replace(
                match.group(0), json_module.dumps(env_var_value).decode("utf-8")
            )
        elif env_var_type == ":int":
            json_string = json_string.replace(
                match.group(0), json_module.dumps(int(env_var_value)).decode("utf-8")
            )
        elif env_var_type == ":float":
            json_string = json_string.replace(",", ".")
            json_string = json_string.replace(
                match.group(0), json_module.dumps(float(env_var_value)).decode("utf-8")
            )
        else:
            json_string = (
                json_string.replace("'", '"')
                .replace('"', "'")
                .replace("True", "true")
                .replace("False", "false")
                .replace("None", "null")
            )
            if env_var_type == ":bool":
                json_string = json_string.replace(match.group(0), env_var_value)
            elif env_var_type == ":list":
                json_string = json_string.replace(match.group(0), env_var_value)
            else:
                raise ValueError(
                    f'Environment variable "{env_var_name}" has invalid type "{env_var_type}"'
                )
    return json_string


def get_config(json_string: str) -> ConfigModel:
    """
    Get config from the json string
    :param json_string: json string
    :return: ConfigModel
    """
    json_string = replace_with_values_from_environment_variables(json_string)
    _config = get_json().loads(json_string)
    return ConfigModel(**_config)
