from enum import Enum


class EventType(Enum):
    """Event types.

    * TIMER: Timer event, triggered by EventEngine.
    * TICK: Tick event, contains market data.
    * TRADE: Trade event, contains trade data.
    * ORDER: Order event, contains order data.
    * POSITION: Position event, contains position data.
    * ACCOUNT: Account event, contains account data.
    * CONTRACT: Contract event, contains contract data.
    """

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
    """Order direction.

    * LONG: Long position.
    * SHORT: Short position.
    """

    LONG = "LONG"
    SHORT = "SHORT"


class Exchange(Enum):
    """Supported exchanges.

    * SMART: IBKR SmartRouting.
    * IBKRATS: IBKR Alternative Trading System.
    """

    SMART = "SMART"
    IBKRATS = "IBKRATS"


class Interval(Enum):
    """Timeframe intervals.

    * MINUTE: Minute-basis.
    * HOUR: Hour-basis.
    * DAY: Day-basis.
    """

    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class Offset(Enum):
    """Order offsets.

    * OPEN: Open position.
    * CLOSE: Close position.
    """

    OPEN = "OPEN"
    CLOSE = "CLOSE"


class OptionType(Enum):
    """Option types.

    * CALL: Call option.
    * PUT: Put option.
    """

    CALL = "CALL"
    PUT = "PUT"


class OrderType(Enum):
    """Order types.

    * MARKET: Market order.
    * LIMIT: Limit order.
    * STOP_LOSS: Stop loss order.
    * STOP_LIMIT: Stop limit order.
    * TRAILING_STOP: Trailing stop order.
    """

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"


class Status(Enum):
    """Order statuses.

    * SUBMITTING: Order is submitting.
    * PENDING: Order is pending.
    * PARTIALLY_FILLED: Order is partially filled.
    * FILLED: Order is filled.
    * CANCELLING: Order is cancelling.
    * CANCELLED: Order is cancelled.
    * REJECTED: Order is rejected.
    """

    SUBMITTING = "SUBMITTING"
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Product(Enum):
    """Suuported products.

    * EQUITY: Equity.
    * FUTURES: Futures.
    * OPTION: Option.
    * FOREX: Forex.
    """

    EQUITY = "EQUITY"
    FUTURES = "FUTURES"
    OPTION = "OPTION"
    FOREX = "FOREX"
