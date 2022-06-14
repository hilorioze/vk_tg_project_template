import importlib
import pkgutil

__all__ = ("bps",)


def _get_blueprints():
    for loader, name, is_pkg in pkgutil.walk_packages(
        importlib.import_module("src.blueprints").__path__
    ):
        if is_pkg:
            continue
        module = loader.find_module(name).load_module()
        if hasattr(module, "bp"):
            yield module.bp
        if hasattr(module, "blueprint"):
            yield module.blueprint


bps = list(_get_blueprints())
