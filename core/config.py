import yaml
import os
import re
from pathlib import Path
from functools import lru_cache
from pydantic import ValidationError
from core.models.settings import Settings


ENV_PATTERN = re.compile(r"\$\{([^}^{]+)\}")


def resolve_env_vars(value: str) -> str:
    """Replace ${VAR} inside YAML with environment variables."""
    if not isinstance(value, str):
        return value

    matches = ENV_PATTERN.findall(value)
    for var in matches:
        env_value = os.getenv(var)
        if env_value is None:
            raise RuntimeError(f"Missing required environment variable: {var}")
        value = value.replace("${" + var + "}", env_value)

    return value


def load_raw_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    # recursively replace env vars
    def walk(node):
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        elif isinstance(node, list):
            return [walk(v) for v in node]
        else:
            return resolve_env_vars(node)

    return walk(raw)


@lru_cache
def get_config() -> Settings:
    cfg_path = Path("config/settings.yaml")
    if not cfg_path.exists():
        raise FileNotFoundError("Missing config/settings.yaml")

    data = load_raw_yaml(cfg_path)

    try:
        return Settings(**data)
    except ValidationError as e:
        print("❌ Configuration validation failed:")
        print(e)
        raise
