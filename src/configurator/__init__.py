# -*- coding: utf-8 -*-
import os
import typing
from pathlib import Path

from src.configurator.utils import get_config

__all__ = ("config",)


def find_file(
    file_name: str,
    base_dir: typing.Optional[typing.Union[str, bytes, os.PathLike]] = None,
) -> typing.Optional[Path]:
    """
    Finds a file in the current directory or in parent directories.
    :param file_name: The name of the file to find.
    :param base_dir: The base directory to start searching from.
    :return: The path to the file if found, None otherwise.
    """
    if base_dir:
        assert os.path.isdir(base_dir), f"{base_dir!r} is not a directory"
        _base_dir = Path(base_dir)  # type: ignore
    else:
        _base_dir = Path(__file__)
    _base_dir = _base_dir.absolute()
    if (_base_dir / file_name).is_file():
        return _base_dir / file_name
    parents = _base_dir.parents
    for parent in parents:
        file = parent / file_name
        if file.is_file():
            return file.absolute()
    return None


_config_path = find_file("config.json")
if _config_path is None:
    raise FileNotFoundError("config.json not found")

with open(_config_path, "r") as f:
    config = get_config(f.read())
