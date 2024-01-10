from enigma.core.engine import BaseEngine


class BasePackage:
    package_name: str
    engine_class: type[BaseEngine]
