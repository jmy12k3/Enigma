from enum import Enum


class Direction(Enum):
    """Order directions.

    * LONG: Buy.
    * SHORT: Sell.
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
    """Supported timeframes.

    * MINUTE: Aggregated by a minute-basis.
    * HOUR: Aggregated by an hour-basis.
    * DAY: Aggregated by a day-basis.
    """

    MINUTE = "MINUTELY"
    HOUR = "HOURLY"
    DAY = "DAY"


class Offset(Enum):
    """Account offsets.

    * OPEN: Open a new position.
    * CLOSE: Close an existing position.
    """

    OPEN = "OPEN"
    CLOSE = "CLOSE"


class OptionType(Enum):
    """Option types.

    * CALL: A call option is an agreement that gives the option buyer
    the right to buy the underlying asset at a specified price within
    a specific time period.

    * PUT: A put option is an agreement that gives the option buyer
    the right to sell the underlying asset at a specified price within
    a specific time period.
    """

    CALL = "CALL"
    PUT = "PUT"


class OrderType(Enum):
    """Order types.

    * MARKET: A market order is a buy or sell order to be executed
    immediately at the current market prices.

    * LIMIT: A limit order is a buy or sell order to be executed at a
    specified price or better.

    * STOP_LOSS: A stop-loss order is an order placed with a broker to
    buy or sell a security when it reaches a certain price.

    * STOP_LIMIT: A stop-limit order is an order placed with a broker
    that combines the features of a stop order with those of a limit
    order.

    * TRAILING_STOP: A trailing stop is a stop order that can be set at
    a defined percentage or dollar amount away from a security's current
    market price.
    """

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"


class Status(Enum):
    """Order statuses.

    * SUBMITTING: The order is being submitted.
    * PENDING: The order is pending.
    * PARTIALLY_FILLED: The order is partially filled.
    * FILLED: The order is filled.
    * CANCELLING: The order is being cancelled.
    * CANCELLED: The order is cancelled.
    * REJECTED: The order is rejected.
    """

    SUBMITTING = "SUBMITTING"
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Product(Enum):
    """Suuported financial products.

    * EQUITY: A stock or any other security representing an ownership
    interest.

    * FUTURES: A financial contract obligating the buyer to purchase an
    asset or the seller to sell an asset, such as a commodity or
    financial instrument, at a predetermined future date and price.

    * OPTION: A contract that gives the buyer the right, but not the
    obligation, to buy or sell an underlying asset at a specific price
    on or before a certain date.

    * FOREX: The foreign exchange market is a global decentralized or
    over-the-counter market for the trading of currencies.
    """

    EQUITY = "EQUITY"
    FUTURES = "FUTURES"
    OPTION = "OPTION"
    FOREX = "FOREX"
