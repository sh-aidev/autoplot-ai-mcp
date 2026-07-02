"""
Application-specific exception hierarchy.
"""


class AppException(Exception):
    """Base exception for application-specific errors."""

    def __init__(self, message: str) -> None:
        """
        Args:
            message (str): Human-readable description of the error.
        """
        self.message = message
        super().__init__(message)


class ToolExecutionError(AppException):
    """Raised when an MCP tool fails to execute."""
    pass
