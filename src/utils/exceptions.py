class AppException(Exception):
    """Base exception for application-specific errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ToolExecutionError(AppException):
    """Raised when an MCP tool fails to execute."""
    pass
