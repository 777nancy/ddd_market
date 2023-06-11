import os

from dotenv import load_dotenv

from marketanalysis.settings.constants import *

ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")


if ENVIRONMENT == "local":
    env_path = os.path.join(CONFIG_DIR, "local.env")
    load_dotenv(env_path)
    from marketanalysis.settings.local import *
