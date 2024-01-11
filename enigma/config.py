"""Config in twelve-factor standard."""

from dynaconf import Dynaconf
from tzlocal import get_localzone_name

ENVVAR_PREFIX = __package__.upper()

CONFIG = {
    "DATABASE_NAME": "",
    "DATABASE_DATABASE": "",
    "DATABASE_HOST": "",
    "DATABASE_PORT": "",
    "DATABASE_USER": "",
    "DATABASE_PASSWORD": "",
    "DATAFEED_NAME": "",
    "DATAFEED_USERNAME": "",
    "DATAFEED_PASSWORD": "",
}
CONFIG["DATABASE_TIMEZONE"] = get_localzone_name()

CONFIG = {f"{ENVVAR_PREFIX}{k}": v for k, v in CONFIG.items()}

CONFIG.update(Dynaconf(envvar_prefix=ENVVAR_PREFIX, load_dotenv=True).to_dict())
