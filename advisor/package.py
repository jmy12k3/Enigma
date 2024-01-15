from advisor.interface import Interface


class Package:
    """Provide a very basic package manifest."""

    package_name: str
    interface_class: type[Interface]
