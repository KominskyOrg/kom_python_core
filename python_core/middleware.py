from flask import request, g
import uuid


def generate_correlation_id():
    return request.headers.get('X-Correlation-ID') or str(uuid.uuid4())


def correlation_id_middleware(app):
    @app.before_request
    def set_correlation_id():
        g.correlation_id = generate_correlation_id()

    @app.after_request
    def add_correlation_id(response):
        response.headers['X-Correlation-ID'] = g.correlation_id
        return response