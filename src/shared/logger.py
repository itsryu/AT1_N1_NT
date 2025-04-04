import logging
import sys
from shared.style import ColorFormatter

_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(ColorFormatter("%(asctime)s - %(levelname)s - %(message)s"))

_logger = logging.getLogger("AppLogger")
_logger.setLevel(logging.DEBUG)
_logger.handlers.clear()
_logger.addHandler(_handler)

class Logger:
    @staticmethod
    def debug(msg: str) -> None:
        _logger.debug(msg)

    @staticmethod
    def info(msg: str) -> None:
        _logger.info(msg)

    @staticmethod
    def warning(msg: str) -> None:
        _logger.warning(msg)

    @staticmethod
    def error(msg: str) -> None:
        _logger.error(msg)

    @staticmethod
    def critical(msg: str) -> None:
        _logger.critical(msg)