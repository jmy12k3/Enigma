"""Twelve-Factor standard configuration."""

import tzlocal
from dynaconf import Dynaconf

# If not specified, the database timezone will be set to the local timezone.
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

# Load the configuration from dotenv file and environment variables.
CONFIG.update(Dynaconf(load_dotenv=True, envvar_prefix=False).to_dict())
