from enum import Enum


class EventType(Enum):
    TIMER = "TIMER"
    TICK = "TICK"
    TRADE = "TRADE"
    POSITION = "POSITION"
    ORDER = "ORDER"
    ACCOUNT = "ACCOUNT"
    CONTRACT = "CONTRACT"

    def __str__(self) -> str:
        return self.value


class Direction(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class Exchange(Enum):
    SMART = "SMART"
    IBKRATS = "IBKRATS"


class Interval(Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class Offset(Enum):
    NONE = "NONE"
    OPEN = "OPEN"
    CLOSE = "CLOSE"


class OptionType(Enum):
    CALL = "CALL"
    PUT = "PUT"


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"


class Status(Enum):
    SUBMITTING = "SUBMITTING"
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Product(Enum):
    EQUITY = "EQUITY"
    FUTURES = "FUTURES"
    OPTION = "OPTION"
    FOREX = "FOREX"
