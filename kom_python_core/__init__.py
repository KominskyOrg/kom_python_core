# python_core/__init__.py

from .logging import LoggingConfig as LoggingConfig
from .http_client import HTTPClient as HTTPClient


def initialize(app, log_level="INFO", env="staging"):
    logger = LoggingConfig(log_level=log_level, environment=env)
    logger.configure()
