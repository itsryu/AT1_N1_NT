import logging
import sys

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",    # Blue
        "INFO": "\033[92m",     # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",    # Red
        "CRITICAL": "\033[95m", # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        return f"{color}{super().format(record)}{self.RESET}"

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