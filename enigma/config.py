import os
import re

import dotenv

_PREFIXES = f"{__package__.upper()}_"
_REGEX = re.compile(rf"{_PREFIXES}\w+")

CONFIG = {
    k.replace(_PREFIXES, "").upper(): v
    for k, v in {
        **dotenv.dotenv_values(".env"),
        **{k: v for k, v in os.environ.items() if _REGEX.match(k)},
    }.items()
}
