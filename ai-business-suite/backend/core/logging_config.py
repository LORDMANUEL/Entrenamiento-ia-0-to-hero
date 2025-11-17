import logging
import os
from .config import settings

def setup_logging():
    """Set up logging configuration."""
    log_dir = settings.PATH_LOGS
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "backend.log")

    logging.basicConfig(
        level=logging.INFO if not settings.DEBUG else logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logging.getLogger("uvicorn").propagate = False
