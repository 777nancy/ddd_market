import os

# PROJECT_BUCKET_NAME = "/workspace/data"
PROJECT_BUCKET_NAME = "/workspace/data"
CHANNEL_ID = os.environ.get("CHANNEL_ID")
TOKEN = os.environ.get("TOKEN")

POSTGRES_USER = os.environ.get("POSTGRES_USER", "test")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "test")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "test")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "test")
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", "test")
