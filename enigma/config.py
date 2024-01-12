import os
import re

import dotenv

_PREFIX = __package__.upper()
_REGEX = re.compile(rf"{_PREFIX}\w+")

CONFIG = {
    **dotenv.dotenv_values(".env"),
    **{k.replace(_PREFIX, ""): v for k, v in os.environ.items() if _REGEX.match(k)},
}
