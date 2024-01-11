"""Config in twelve-factor standard."""

import dynaconf
import tzlocal

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
CONFIG["DATABASE_TIMEZONE"] = tzlocal.get_localzone_name()

CONFIG.update(dynaconf.Dynaconf(envvar_prefix=False, load_dotenv=True).to_dict())
