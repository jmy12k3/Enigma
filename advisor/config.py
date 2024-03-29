import os
import re
from functools import cache
from typing import Any

from dotenv import dotenv_values
from tzlocal import get_localzone_name


@cache
def _get_config(*, prefixes: str = f"{__package__.upper()}_") -> dict[str, Any]:
    regex = re.compile(rf"{prefixes}\w+")

    return {
        k.replace(prefixes, "").upper(): v
        for k, v in {
            "DATABASE_TIMEZONE": get_localzone_name(),
            **dotenv_values(".env"),
            **{k: v for k, v in os.environ.items() if regex.match(k)},
        }.items()
    }


CONFIG = _get_config()
