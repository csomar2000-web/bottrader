import os
from dotenv import load_dotenv
from pathlib import Path

def load_environment():
    """Load environment variables from .env file when running locally."""
    env_path = Path('.') / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print("[env] No .env file found, relying on system env vars.")

def get_env(key: str, default: str | None = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value
