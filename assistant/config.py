import os
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"


def load_config():
    # Load .env from project root if present
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH)
    else:
        # attempt to load from environment
        load_dotenv()


def get(key: str, default=None):
    return os.getenv(key, default)


def bool_get(key: str, default=False):
    val = os.getenv(key)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "y")
