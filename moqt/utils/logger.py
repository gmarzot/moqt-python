import logging
import json
import sys
from logging import getLevelName
from typing import Optional, Dict
from aioquic.quic.logger import QuicLogger

# Cache to store created loggers
_loggers: Dict[str, logging.Logger] = {}

_level = None
_handler = None


def set_log_level(level: any = None) -> any:
    """Set configured log level."""
    global _level
    _level = level
    for logger in _loggers.values():
        logger.setLevel(level)

    return level


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Get a logger with consistent formatting."""
    global _level, _handler

    if name in _loggers:
        logger = _loggers[name]
    else:
        logger = logging.getLogger(name)
        _loggers[name] = logger

    if not logger.handlers:  # Only add handler if none exists
        if _handler is None:
            handler = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter(
                fmt='%(asctime)s.%(msecs)03d %(levelname)-5s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            _handler = handler

        logger.addHandler(_handler)

    if _level is not None:
        level = _level
    else:
        level = logging.INFO
    logger.setLevel(level)
    logger.debug(f"setLevel: level:{getLevelName(level)} name: {name} ")

    return logger


class QuicLoggerCustom(QuicLogger):
    def __init__(self):
        super().__init__()
        self.logger = get_logger('quic_logger', logging.DEBUG)
        # self.logger.debug(f"QUIC debug logger added")

    def log_event(self, event_type: str, data: dict) -> None:
        self.logger.debug(f"QUIC: {event_type}")
        self.logger.debug(json.dumps(data, indent=2))
