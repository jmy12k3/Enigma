import os
import re

import dotenv

_PREFIXES = f"{__package__.upper()}_"

_REGEX = re.compile(rf"{_PREFIXES}\w+")

CONFIG = {
    **dotenv.dotenv_values(".env"),
    **{k.replace(_PREFIXES, ""): v for k, v in os.environ.items() if _REGEX.match(k)},
}
