import logging
import logging.config
import re

from .config import LOGGING
from config.settings.base import app


class Logger:
    def __init__(self) -> None:
        self._config = LOGGING
        self._loging_name = app.name

    def get(self) -> logging:
        logging.config.dictConfig(self._config)
        return logging.getLogger(self._loging_name)

    def sanitize_message(self, message: str) -> str:
        """Sanitize the message by removing newlines, tabs,
             and replacing them with spaces."""
        return re.sub(r'[\n\r\t]', ' ', message)
