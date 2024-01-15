import logging
import sys
from functools import cache
from typing import Any, TextIO

import structlog

from advisor import __version__


@cache
def _get_logger(*, stream: TextIO) -> Any:
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
                structlog.processors.TimeStamper("iso"),
                structlog.processors.CallsiteParameterAdder(
                    {
                        structlog.processors.CallsiteParameter.FILENAME,
                        structlog.processors.CallsiteParameter.FUNC_NAME,
                        structlog.processors.CallsiteParameter.LINENO,
                    }
                ),
                structlog.processors.dict_tracebacks,
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
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(format="%(message)s", level=level, stream=stream)

    return structlog.get_logger()


logger = _get_logger(stream=sys.stdout)
