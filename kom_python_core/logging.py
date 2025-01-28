import logging
import logging.config
import os
from pythonjsonlogger import jsonlogger


class LoggingConfig:
    """Centralized logging configuration."""

    def __init__(self, log_level="INFO", environment="staging", log_dir="logs", max_bytes=10 * 1024 * 1024, backup_count=5):
        self.log_level = log_level.upper()
        self.environment = environment
        self.log_dir = log_dir
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        try:
            os.makedirs(self.log_dir, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create log directory {self.log_dir}: {e}")

    def configure(self):
        """Configures logging settings."""
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": jsonlogger.JsonFormatter,
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(environment)s",
                },
            },
            "filters": {
                "contextual": {
                    "()": self.ContextFilter,
                    "environment": self.environment,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "filters": ["contextual"],
                    "level": self.log_level,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "json",
                    "filters": ["contextual"],
                    "level": "INFO",
                    "filename": os.path.join(self.log_dir, "app.log"),
                    "maxBytes": self.max_bytes,
                    "backupCount": self.backup_count,
                    "encoding": "utf8",
                },
            },
            "loggers": {
                "": {  # root logger
                    "handlers": ["console", "file"],
                    "level": self.log_level,
                    "propagate": True,
                },
                "exceptions": {
                    "handlers": ["console", "file"],
                    "level": "ERROR",
                    "propagate": False,
                },
            },
        }

        logging.config.dictConfig(logging_config)

    def set_log_level(self, level: str):
        """Dynamically update log level for all handlers."""
        level = level.upper()
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        for handler in root_logger.handlers:
            handler.setLevel(level)

    class ContextFilter(logging.Filter):
        """Adds contextual information to logs."""
        def __init__(self, environment):
            super().__init__()
            self.environment = environment

        def filter(self, record):
            record.environment = self.environment
            return True
