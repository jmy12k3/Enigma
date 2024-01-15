from abc import ABC, abstractmethod
from datetime import datetime

from advisor.config import CONFIG
from advisor.logger import logger
from advisor.models import (
    BarData,
    BarOverview,
    Exchange,
    Interval,
    TickData,
    TickOverview,
)
from advisor.packages import import_package


class DatabasePackageError(Exception):
    """Provide an exception for the database package."""


class Database(ABC):
    """Provide an abstract base class for the database package."""

    @abstractmethod
    def save_bar_data(self, bars: list[BarData], *, stream: bool = False) -> bool:
        ...

    @abstractmethod
    def save_tick_data(self, ticks: list[TickData], *, stream: bool = False) -> bool:
        ...

    @abstractmethod
    def load_bar_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime,
    ) -> list[BarData]:
        ...

    @abstractmethod
    def load_tick_data(
        self,
        symbol: str,
        exchange: Exchange,
        start: datetime,
        end: datetime,
    ) -> list[TickData]:
        ...

    @abstractmethod
    def delete_bar_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
    ) -> int:
        ...

    @abstractmethod
    def delete_tick_data(self, symbol: str, exchange: Exchange) -> int:
        ...

    @abstractmethod
    def get_bar_overview(self) -> list[BarOverview]:
        ...

    @abstractmethod
    def get_tick_overview(self) -> list[TickOverview]:
        ...


class DatabaseSingletonMeta(type):
    """Provide a metaclass for the function-like database singleton."""

    _database: Database | None = None

    def __call__(cls) -> Database | None:
        if not cls._database:
            database_name = CONFIG["DATABASE_NAME"]

            try:
                package = import_package(database_name)

                cls._database = package.Database()

                logger.info(
                    "Initialized database",
                    database_name=database_name,
                )
            except DatabasePackageError:
                cls._database = None

                logger.error(
                    "Failed to initialize database",
                    database_name=database_name,
                )

        return cls._database


class DatabaseSingleton(metaclass=DatabaseSingletonMeta):
    """Provide a function-like database singleton."""
