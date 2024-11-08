import logging
from functools import wraps
from flask import jsonify
from .error_handler import APIError

logger = logging.getLogger(__name__)

def handle_request(service_function):
    @wraps(service_function)
    def wrapper(*args, **kwargs):
        logger.info(f"Handling request for {service_function.__name__}")
        logger.debug(f"Arguments: args={args}, kwargs={kwargs}")
        try:
            response, status_code = service_function(*args, **kwargs)
            logger.debug(
                f"Service function response: {response}, Status code: {status_code}"
            )
            return jsonify(response), status_code
        except APIError as ae:
            logger.warning(
                f"{ae.__class__.__name__} in {service_function.__name__}: {ae.message}"
            )
            return jsonify({
                "error": {
                    "code": ae.error_code,
                    "message": ae.message
                }
            }), ae.status_code
        except Exception as e:
            logger.exception(f"Unexpected error in {service_function.__name__}: {e}")
            return jsonify({
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Internal server error"
                }
            }), 500
    return wrapper