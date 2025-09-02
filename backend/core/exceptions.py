class AppException(Exception):
    """Base application exception."""

    status_code: int = 500
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None):
        if message is not None:
            self.message = message

    def __str__(self) -> str:
        return self.message


class UnauthorizedException(AppException):
    """Exception raised for unauthorized access."""

    status_code = 401
    message = "Unauthorized"


class ForbiddenException(AppException):
    """Exception raised for forbidden access."""

    status_code = 403
    message = "Forbidden"


class UnprocessableEntityException(AppException):
    """Exception raised for unprocessable entities."""

    status_code = 422
    message = "Unprocessable Entity"
