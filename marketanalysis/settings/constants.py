import os

PROJECT_NAME = "marketanalysis"
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SRC_ROOT_DIR = os.path.join(PROJECT_ROOT_DIR, PROJECT_NAME)
RESOURCES_DIR = os.path.join(SRC_ROOT_DIR, "resources")
CONFIG_DIR = os.path.join(PROJECT_ROOT_DIR, "config")

SLACK_FILE_URL = "https://slack.com/api/files.upload"
CHANNEL_ID = ""
TOKEN = ""

# POSTGRES_USER = "root"
# POSTGRES_PASSWORD = "root"
# POSTGRES_HOST = "postgres"
# POSTGRES_PORT = "5432"
# POSTGRES_DATABASE = "market"

# stop_limitのデフォルト値
STOP_LIMIT = 0.04
