import os
import re

import dotenv

_PREFIX = __package__.upper()
_REGEX = re.compile(rf"{_PREFIX}\w+")
_ENVIRONS = {
    k.replace(_PREFIX, ""): v for k, v in os.environ.items() if _REGEX.match(k)
}

CONFIG = {**dotenv.dotenv_values(".env"), **_ENVIRONS}
