from collections import defaultdict
from collections.abc import Callable
from contextlib import suppress
from queue import Empty, Queue
from threading import Thread
from time import sleep

from advisor.models import Event, EventType

_T = Callable[[Event], None]


class Engine:
    def __init__(self, interval: int = 1) -> None:
        self._interval = interval
        self._queue: Queue[Event] = Queue()
        self._active = False
        self._thread = Thread(target=self._run)
        self._timer = Thread(target=self._run_timer)
        self._handlers: defaultdict[EventType, list[_T]] = defaultdict(list)

    def _run(self) -> None:
        while self._active:
            with suppress(Empty):
                self._process(self._queue.get(block=True, timeout=1))

    def _process(self, event: Event) -> None:
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                handler(event)

    def _run_timer(self) -> None:
        while self._active:
            sleep(self._interval)
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

    def unregister(self, type: EventType, handler: _T) -> None:
        handler_list = self._handlers[type]
        if handler in handler_list:
            handler_list.remove(handler)
        if not handler_list:
            del self._handlers[type]
