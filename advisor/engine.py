import time
from collections import defaultdict
from collections.abc import Callable
from contextlib import suppress
from queue import Empty, Queue
from threading import Thread

from advisor.models import Event, EventType

_T = Callable[[Event], None]


class Engine:
    """The underlying event-driven engine of the whole framework."""

    def __init__(self) -> None:
        # Queue to store events
        self._queue: Queue[Event] = Queue()

        # Flag to indicate whether the engine is active
        self._active = False

        # Thread to run the engine
        self._engine = Thread(target=self._run)

        # Thread to run the clock
        self._clock = Thread(target=self._run_clock)

        # Dictionary to store event handlers for each event type
        self._handlers: defaultdict[EventType, list[_T]] = defaultdict(list)

    def _run(self) -> None:
        """Run the engine. This method is intended to be called in a separate thread."""
        while self._active:
            with suppress(Empty):
                self._process(self._queue.get(block=True, timeout=1))

    def _process(self, event: Event) -> None:
        """Process an event.

        This method calls all registered handlers for the event's type.

        Parameters
        ----------
        event : Event
            The event to process.
        """
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                handler(event)

    def _run_clock(self) -> None:
        """Run the clock. This method is intended to be called in a separate thread."""
        while self._active:
            time.sleep(1)
            self.put(Event(EventType.CLOCK))

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

    def put(self, event: Event) -> None:
        """Put an event to the queue.

        Parameters
        ----------
        event : Event
            The event to put to the queue.
        """
        self._queue.put(event)

    def register(self, type: EventType, handler: _T) -> None:
        """Register a handler for a specfic event type.

        Parameters
        ----------
        type : EventType
            The type of the event to register the handler for.
        handler : _T
            The handler to register.
        """
        handler_list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type: EventType, handler: _T) -> None:
        """Unregister a handler for a specific event type.

        Parameters
        ----------
        type : EventType
            The type of the event to unregister the handler for.
        handler : _T
            The handler to unregister.
        """
        handler_list = self._handlers[type]
        if handler in handler_list:
            handler_list.remove(handler)
        if not handler_list:
            del self._handlers[type]
