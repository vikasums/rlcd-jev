"""
Configuration Loader reading from environment variables (.env).
Follows Code Style Guidelines: No hardcoded paths, API keys, or model names.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

def load_dotenv(dotenv_path: Optional[Path] = None):
    """Simple lightweight .env parser without external dependencies."""
    path = dotenv_path or Path(".env")
    if path.is_file():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())

load_dotenv()

@dataclass
class Settings:
    typesafe_api_key: str = field(default_factory=lambda: os.getenv("TYPESAFE_API_KEY", ""))
    typesafe_base_url: str = field(default_factory=lambda: os.getenv("TYPESAFE_BASE_URL", "https://api.typesafe.ai/v1"))
    typesafe_model_name: str = field(default_factory=lambda: os.getenv("TYPESAFE_MODEL_NAME", "jev-rlcd-v1"))

    system_two_provider: str = field(default_factory=lambda: os.getenv("SYSTEM_TWO_PROVIDER", "openai"))
    system_two_api_key: str = field(default_factory=lambda: os.getenv("SYSTEM_TWO_API_KEY", ""))
    system_two_model_name: str = field(default_factory=lambda: os.getenv("SYSTEM_TWO_MODEL_NAME", "gpt-4o"))

    confidence_threshold: float = field(default_factory=lambda: float(os.getenv("FIREWALL_CONFIDENCE_THRESHOLD", "0.90")))
    enable_db_audit: bool = field(default_factory=lambda: os.getenv("FIREWALL_ENABLE_DB_AUDIT", "true").lower() == "true")
    environment: str = field(default_factory=lambda: os.getenv("FIREWALL_ENV", "development"))

    database_path: str = field(default_factory=lambda: os.getenv("DATABASE_PATH", "data/audit_logs.db"))
    secret_key_path: str = field(default_factory=lambda: os.getenv("SECRET_KEY_PATH", "secret_key"))

settings = Settings()
