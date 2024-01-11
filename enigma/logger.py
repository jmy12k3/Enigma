"""Logging in twelve-factor standard."""

import functools
import logging
import sys
import typing

import structlog


@functools.cache
def _logger(*, stream: typing.TextIO) -> typing.Any:
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

    structlog.configure(
        processors,
        structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(format="%(message)s", level=level, stream=stream)

    return structlog.get_logger()


logger = _logger(stream=sys.stdout)
