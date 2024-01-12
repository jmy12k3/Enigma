from enigma.interface import Interface


class Module:
    module_name: str
    interface_class: type[Interface]
