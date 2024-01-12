"""A loguru-like, twelve-factor standard logger."""

import logging
import sys
import typing

import structlog

from . import __version__


def _set_logger(*, stream: typing.TextIO) -> None:
    shared_processors: list[structlog.typing.Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
    ]
    processors: list[structlog.typing.Processor] = [*shared_processors]

    if stream.isatty():
        level = logging.DEBUG
        processors.extend(
            [
                structlog.processors.TimeStamper("%Y-%m-%d %H:%M:%S", utc=False),
                structlog.dev.ConsoleRenderer(),
            ],
        )
    else:
        level = logging.INFO
        processors.extend(
            [
                structlog.processors.dict_tracebacks,
                structlog.processors.TimeStamper("iso"),
                structlog.processors.JSONRenderer(),
            ],
        )

        structlog.contextvars.bind_contextvars(
            build_info={
                "version": __version__,
                "python_version": sys.version,
            }
        )

    structlog.configure(
        processors,
        structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(format="%(message)s", level=level, stream=stream)


_set_logger(stream=sys.stdout)

logger = structlog.get_logger()
