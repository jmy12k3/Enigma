import time
from collections import defaultdict
from collections.abc import Callable
from queue import Empty, Queue
from threading import Thread

from enigma.core.enum import EventType
from enigma.core.logging import logger
from enigma.core.object import Event

_T = Callable[[Event], None]


class EventEngine:
    def __init__(self, interval: int = 1) -> None:
        self._interval = interval
        self._queue: Queue[Event] = Queue()
        self._active = False
        self._thread = Thread(target=self._run)
        self._timer = Thread(target=self._run_timer)
        self._handlers: defaultdict[EventType, list[_T]] = defaultdict(list)

    def _run(self) -> None:
        while self._active:
            try:
                event: Event = self._queue.get(block=True, timeout=1)
                self._process(event)
            except Empty:
                pass

    def _process(self, event: Event) -> None:
        if event.type in self._handlers:
            [handler(event) for handler in self._handlers[event.type]]

    def _run_timer(self) -> None:
        while self._active:
            time.sleep(self._interval)
            self.put(Event(EventType.TIMER))

    def start(self) -> None:
        self._active = True
        self._thread.start()
        self._timer.start()

    def stop(self) -> None:
        self._active = False
        self._timer.join()
        self._thread.join()

    def put(self, event: Event) -> None:
        self._queue.put(event)

    def register(self, type: EventType, handler: _T) -> None:
        handler_list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)
            logger.debug(
                "Registered event handler",
                Event=str(type),
                Handler=handler.__name__,
            )

    def unregister(self, type: EventType, handler: _T) -> None:
        handler_list = self._handlers[type]
        if handler in handler_list:
            handler_list.remove(handler)
            logger.debug(
                "Unregistered event handler",
                event=str(type),
                handler=handler.__name__,
            )
        if not handler_list:
            del self._handlers[type]
