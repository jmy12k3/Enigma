"""Config in twelve-factor standard."""

import dynaconf
import tzlocal

# set envvar_prefix as package name in upper case
ENVVAR_PREFIX = __package__.upper()

# set default values for optional settings
# note that dotenv config does not support nested structures
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

# set default values for mandatory setting
CONFIG["DATABASE_TIMEZONE"] = tzlocal.get_localzone_name()

# append envvar_prefix to default config
CONFIG = {f"{ENVVAR_PREFIX}{k}": v for k, v in CONFIG.items()}

# load config from environment variables and dotenv file
CONFIG.update(
    dynaconf.Dynaconf(
        envvar_prefix=ENVVAR_PREFIX,
        load_dotenv=True,
    ).to_dict()
)
