import logging
import logging.config
from .config import LOGGING
from config.settings.base import APP


class Logger:
    def __init__(self) -> None:
        self._config = LOGGING
        self._loging_name = APP.name

    def get(self) -> logging:
        logging.config.dictConfig(self._config)
        return logging.getLogger(self._loging_name)
