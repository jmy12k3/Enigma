from advisor.interface import Interface


class Package:
    package_name: str
    interface_class: type[Interface]
