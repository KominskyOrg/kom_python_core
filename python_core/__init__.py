# python_core/__init__.py

from .logging import configure_logging
from .middleware import correlation_id_middleware
from .tracing import configure_tracing
from .http_client import HTTPClient


def initialize(app):
    configure_logging()
    correlation_id_middleware(app)
    configure_tracing(app)
