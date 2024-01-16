from importlib import import_module
from types import ModuleType


class PackageImportError(Exception):
    """Provide an exception for the package import."""


def import_package(package_name: str) -> ModuleType:
    return import_module(f".{package_name}", __package__)
