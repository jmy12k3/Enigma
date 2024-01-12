import functools
import os
import re
from typing import Any

import dotenv


@functools.cache
def _get_config() -> dict[str, Any]:
    prefixes = f"{__package__.upper()}_"
    regex = re.compile(rf"{prefixes}\w+")

    return {
        k.replace(prefixes, "").upper(): v
        for k, v in {
            **dotenv.dotenv_values(".env"),
            **{k: v for k, v in os.environ.items() if regex.match(k)},
        }.items()
    }


CONFIG = _get_config()
