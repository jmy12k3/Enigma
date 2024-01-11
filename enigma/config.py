"""Config in twelve-factor standard."""

import dynaconf
import tzlocal

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
CONFIG["DATABASE_TIMEZONE"] = tzlocal.get_localzone_name()

CONFIG = {f"{ENVVAR_PREFIX}{k}": v for k, v in CONFIG.items()}

CONFIG.update(
    dynaconf.Dynaconf(
        envvar_prefix=ENVVAR_PREFIX,
        load_dotenv=True,
    ).to_dict()
)
