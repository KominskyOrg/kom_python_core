# python_core/error_handler.py

class APIError(Exception):
    def __init__(self, message, status_code, error_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

class ValidationError(APIError):
    def __init__(self, message, error_code="VALIDATION_ERROR"):
        super().__init__(message, 400, error_code)

class AuthenticationError(APIError):
    def __init__(self, message, error_code="AUTHENTICATION_ERROR"):
        super().__init__(message, 401, error_code)

class AuthorizationError(APIError):
    def __init__(self, message, error_code="AUTHORIZATION_ERROR"):
        super().__init__(message, 403, error_code)

class DatabaseError(APIError):
    def __init__(self, message="Database error occurred", error_code="DATABASE_ERROR"):
        super().__init__(message, 500, error_code)