"""Config in twelve-factor standard."""

import tzlocal
from dynaconf import Dynaconf

# This should be loaded from a .env file
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

# This should be loaded from a environemnetal variable
CONFIG["DATABASE_TIMEZONE"] = tzlocal.get_localzone_name()

CONFIG.update(Dynaconf(envvar_prefix=False, load_dotenv=True).to_dict())
