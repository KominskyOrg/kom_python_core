# central_logging/logging_config.py
import logging
import logging.config
import os

def configure_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(correlation_id)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "level": log_level,
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "level": "INFO",
                "filename": "app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": log_level,
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