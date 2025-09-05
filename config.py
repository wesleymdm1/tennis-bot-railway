import os


def require_env(name: str) -> str:
    """Return environment variable or raise RuntimeError if missing."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value


TELEGRAM_TOKEN = require_env("TELEGRAM_TOKEN")
API_KEY = require_env("API_KEY")
API_HOST = require_env("API_HOST")

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
