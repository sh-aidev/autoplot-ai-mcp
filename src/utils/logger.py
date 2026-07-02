"""
Configures the shared `loguru` logger used across the application and
exposes a ready-to-use `logger` instance.
"""

from loguru import logger
import sys
import os


class Logger:
    """
    Configures `loguru` sinks (rotating file + stderr) for a given environment.
    """

    @staticmethod
    def create_sess(env):
        """
        Resets and reconfigures the `loguru` logger for the given environment.

        Args:
            env (str): Deployment environment, either "dev" or "prod"; controls
                       the stderr log level (DEBUG for "dev", INFO for "prod").

        Returns:
            loguru.Logger: The configured logger instance.
        """
        logger.remove()
        logger.add(
            "outputs/logs/server.log",
            format="{time} {level} {message}",
            rotation="10 MB",
            compression="zip",
            serialize=True,
        )
        env_dict = {"dev": "DEBUG", "prod": "INFO"}
        logger.add(sys.stderr, level=env_dict[env])
        return logger


class Logger_py:
    """
    Builds the module-level `logger` by configuring it from the
    `ENVIRONMENT` environment variable.
    """

    def __init__(self) -> None:
        """
        Configures the logger for the environment named in `ENVIRONMENT`
        (default: "dev") and stores it on `self.logger`.
        """
        self.logger = Logger.create_sess(os.getenv("ENVIRONMENT", "dev"))
        self.logger.info(
            f"Logger for environemnt: {str(os.getenv('ENVIRONMENT', 'dev'))}"
        )

    def run(self) -> Logger:
        """
        Returns:
            loguru.Logger: The configured logger instance.
        """
        return self.logger


logger = Logger_py().run()
