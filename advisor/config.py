import os
import re
from functools import cache
from typing import Any

import dotenv
import tzlocal


@cache
def _get_config(*, prefixes: str = __package__.upper()) -> dict[str, Any]:
    regex = re.compile(rf"{prefixes}\w+")

    return {
        k.replace(prefixes, "").upper(): v
        for k, v in {
            "DATABASE_TIMEZONE": tzlocal.get_localzone_name(),
            **dotenv.dotenv_values(".env"),
            **{k: v for k, v in os.environ.items() if regex.match(k)},
        }.items()
    }


CONFIG = _get_config()
