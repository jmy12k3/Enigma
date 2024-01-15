import queue
import time
from collections import defaultdict
from collections.abc import Callable
from contextlib import suppress
from threading import Thread

from advisor.logger import logger
from advisor.models import Event, EventType

HandlerType = Callable[[Event], None]


class Engine:
    """The underlying event-driven engine of the whole framework."""

    def __init__(self) -> None:
        # Flag to indicate whether the engine is active
        self._active = False

        # Queue to store events
        self._queue: queue.Queue[Event] = queue.Queue()

        # Thread to run the engine
        self._engine = Thread(target=self._run_engine)

        # Thread to run the clock
        self._clock = Thread(target=self._run_clock)

        # Dictionary to store event handlers for each event type
        self._handlers: defaultdict[EventType, list[HandlerType]] = defaultdict(list)

    def _process(self, event: Event) -> None:
        """Process an event."""
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                handler(event)

    def _run_engine(self) -> None:
        """Run the engine."""
        while self._active:
            with suppress(queue.Empty):
                self._process(self._queue.get(block=True, timeout=1))

    def _run_clock(self) -> None:
        """Run the clock."""
        while self._active:
            time.sleep(1)
            self.put(Event(EventType.CLOCK))

    def put(self, event: Event) -> None:
        """Put an event to the queue."""
        self._queue.put(event)

    def start(self) -> None:
        """Start the engine and the clock."""
        self._active = True
        self._engine.start()
        self._clock.start()

    def stop(self) -> None:
        """Stop the engine and the clock."""
        self._active = False
        self._clock.join()
        self._engine.join()

    def register(self, type: EventType, handler: HandlerType) -> None:
        """Register a handler for a specfic event type."""
        handler_list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)
            logger.debug(
                "Registered event handler.",
                event_type=type.value,
                event_handler=handler.__name__,
            )
        else:
            logger.warning(
                "Attempted to register an already registered event handler.",
                event_type=type.value,
                event_handler=handler.__name__,
            )

    def unregister(self, type: EventType, handler: HandlerType) -> None:
        """Unregister a handler for a specific event type."""
        handler_list = self._handlers[type]
        if handler in handler_list:
            handler_list.remove(handler)
            if not handler_list:
                self._handlers.pop(type)
            logger.debug(
                "Unregistered event handler.",
                event_type=type.value,
                event_handler=handler.__name__,
            )
        else:
            logger.warning(
                "Attempted to unregister a non-registered event handler.",
                event_type=type.value,
                event_handler=handler.__name__,
            )
