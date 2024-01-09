from enum import Enum


class EventType(Enum):
    ACCOUNT = "ACCOUNT"
    CONTRACT = "CONTRACT"
    ORDER = "ORDER"
    POSITION = "POSITION"
    TICK = "TICK"
    TIMER = "EVENT_TIMER"
    TRADE = "TRADE"

    def __str__(self) -> str:
        return self.value
