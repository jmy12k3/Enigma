"""Config in twelve-factor standard."""

import tzlocal
from dynaconf import Dynaconf

CONFIG = {
    "DATABASE_TIMEZONE": tzlocal.get_localzone_name(),
    "DATABASE_NAME": "",
    "DATABASE_DATABASE": "",
    "DATABASE_HOST": "",
    "DATABASE_PORT": 0,
    "DATABASE_USER": "",
    "DATABASE_PASSWORD": "",
    "DATAFEED_NAME": "",
    "DATAFEED_USERNAME": "",
    "DATAFEED_PASSWORD": "",
}

CONFIG.update(Dynaconf(envvar_prefix=False, load_dotenv=True).to_dict())
