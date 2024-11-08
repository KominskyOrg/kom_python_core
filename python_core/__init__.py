# python_core/__init__.py

from .logging import configure_logging
from .error_handler import configure_exception_handling
from .middleware import correlation_id_middleware
from .tracing import configure_tracing


def initialize(app):
    configure_logging()
    configure_exception_handling()
    correlation_id_middleware(app)
    configure_tracing(app)
