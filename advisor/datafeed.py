from abc import ABC, abstractmethod

from advisor.config import CONFIG
from advisor.logger import logger
from advisor.models import BarData, HistoryRequest, TickData
from advisor.packages import PackageImportError, import_package


class Datafeed(ABC):
    """Provide an abstract base class for the datafeed package."""

    @abstractmethod
    def query_bar_history(self, req: HistoryRequest) -> list[BarData] | None:
        ...

    @abstractmethod
    def query_tick_history(self, req: HistoryRequest) -> list[TickData] | None:
        ...


class DatafeedSingletonMeta(type):
    """Provide a metaclass for the function-like datafeed singleton."""

    _datafeed: Datafeed | None = None

    def __call__(cls) -> Datafeed | None:
        if not cls._datafeed:
            datafeed_name = CONFIG["DATAFEED_NAME"]

            try:
                package = import_package(datafeed_name)

                cls._datafeed = package.Datafeed()

                logger.info("Initialized datafeed", datafeed_name=datafeed_name)
            except PackageImportError:
                cls._datafeed = None

                logger.error(
                    "Failed to initialize datafeed",
                    datafeed_name=datafeed_name,
                )

        return cls._datafeed


class DatafeedSingleton(metaclass=DatafeedSingletonMeta):
    """Provide a function-like datafeed singleton."""
