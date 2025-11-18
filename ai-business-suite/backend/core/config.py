from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    API_TITLE: str = "AI Business Suite API"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # --- Simplified and Robust Path Settings ---
    # This configuration assumes that the server and any scripts
    # are run from the 'backend' directory.

    # The current working directory will be 'backend', so '.' points to it.
    BACKEND_DIR: Path = Path.cwd()

    # The monorepo root is the parent of the 'backend' directory.
    BASE_DIR: Path = BACKEND_DIR.parent

    PATH_DATA: Path = BASE_DIR / "data"
    PATH_LOGS: Path = BASE_DIR / "logs"
    PATH_MODELS: Path = BACKEND_DIR / "models_ml"

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure the logs directory exists
os.makedirs(settings.PATH_LOGS, exist_ok=True)
