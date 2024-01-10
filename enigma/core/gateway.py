from abc import ABC, abstractmethod
from typing import Any, ClassVar

from enigma.core.event import EventEngine
from enigma.models import (
    AccountData,
    BarData,
    CancelRequest,
    ContractData,
    Event,
    EventType,
    Exchange,
    HistoryRequest,
    OrderData,
    OrderRequest,
    PositionData,
    SubscribeRequest,
    TickData,
    TradeData,
)


class BaseGateway(ABC):
    default_name = ""

    default_setting: ClassVar[dict[str, Any]] = {}

    exchanges: ClassVar[list[Exchange]] = []

    def __init__(self, event_engine: EventEngine, gateway_name: str) -> None:
        self.event_engine = event_engine
        self.gateway_name = gateway_name

    def on_event(self, type: EventType, data: Any = None) -> None:
        event = Event(type, data)
        self.event_engine.put(event)

    def on_tick(self, tick: TickData) -> None:
        self.on_event(EventType.TICK, tick)

    def on_trade(self, trade: TradeData) -> None:
        self.on_event(EventType.TRADE, trade)

    def on_order(self, order: OrderData) -> None:
        self.on_event(EventType.ORDER, order)

    def on_position(self, position: PositionData) -> None:
        self.on_event(EventType.POSITION, position)

    def on_account(self, account: AccountData) -> None:
        self.on_event(EventType.ACCOUNT, account)

    def on_contract(self, contract: ContractData) -> None:
        self.on_event(EventType.CONTRACT, contract)

    @abstractmethod
    def connect(self, setting: dict[str, Any]) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def subscribe(self, req: SubscribeRequest) -> None:
        ...

    @abstractmethod
    def send_order(self, req: OrderRequest) -> str:
        ...

    @abstractmethod
    def cancel_order(self, req: CancelRequest) -> None:
        ...

    @abstractmethod
    def query_account(self) -> None:
        ...

    @abstractmethod
    def query_position(self) -> None:
        ...

    @abstractmethod
    def query_history(self, req: HistoryRequest) -> list[BarData]:
        ...

    def get_default_setting(self) -> dict[str, Any]:
        return self.default_setting
