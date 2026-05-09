"""Configuration utilities for the DataMind application."""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Runtime settings loaded from environment variables."""

    app_name: str = os.getenv("DATAMIND_APP_NAME", "DataMind")
    env: str = os.getenv("DATAMIND_ENV", "development")
    log_level: str = os.getenv("DATAMIND_LOG_LEVEL", "INFO")
    host: str = os.getenv("DATAMIND_HOST", "0.0.0.0")
    port: int = int(os.getenv("DATAMIND_PORT", "8000"))


settings = Settings()
