from abc import ABC, abstractmethod
from typing import Any, ClassVar

from enigma.core.enum import EventType, Exchange
from enigma.core.event import Event, EventEngine
from enigma.core.object import (
    AccountData,
    BarData,
    CancelRequest,
    ContractData,
    HistoryRequest,
    OrderData,
    OrderRequest,
    PositionData,
    SubscribeRequest,
    TickData,
    TradeData,
)

_T = int | float | str | bool


class BaseGateway(ABC):
    default_name = ""

    default_setting: ClassVar[dict[str, _T]] = {}

    exchanges: ClassVar[list[Exchange]] = []

    def __init__(self, event_engine: EventEngine, gateway_name: str) -> None:
        self.event_engine = event_engine
        self.gateway_name = gateway_name

    def get_default_setting(self) -> dict[str, _T]:
        return self.default_setting

    def on_event(self, type: EventType, data: Any = None) -> None:
        event = Event(type, data)
        self.event_engine.put(event)

    def on_account(self, account: AccountData) -> None:
        self.on_event(EventType.ACCOUNT, account)

    def on_contract(self, contract: ContractData) -> None:
        self.on_event(EventType.CONTRACT, contract)

    def on_order(self, order: OrderData) -> None:
        self.on_event(EventType.ORDER, order)

    def on_position(self, position: PositionData) -> None:
        self.on_event(EventType.POSITION, position)

    def on_tick(self, tick: TickData) -> None:
        self.on_event(EventType.TICK, tick)

    def on_trade(self, trade: TradeData) -> None:
        self.on_event(EventType.TRADE, trade)

    @abstractmethod
    def connect(self, setting: dict[str, _T]) -> None:
        ...

    @abstractmethod
    def query_account(self) -> None:
        ...

    @abstractmethod
    def query_position(self) -> None:
        ...

    @abstractmethod
    def cancel_order(self, req: CancelRequest) -> None:
        ...

    @abstractmethod
    def query_history(self, req: HistoryRequest) -> list[BarData]:
        ...

    @abstractmethod
    def send_order(self, req: OrderRequest) -> str:
        ...

    @abstractmethod
    def subscribe(self, req: SubscribeRequest) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
