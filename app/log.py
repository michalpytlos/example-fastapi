import inspect
import logging
import os
import sys

from loguru import logger

from .config import settings


# Recipe from https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    os.makedirs(settings.log.directory, exist_ok=True)

    # Remove the default Loguru handler
    logger.remove()

    # Add console handler
    logger.configure(extra={"user": "-"})
    logger.add(
        sys.stderr,
        level=settings.log.level,
        format="<level>{level}</level> | {name}:{function}:{line} | {message}",
    )

    # Add file handler
    logger.add(
        os.path.join(settings.log.directory, "postboard.log"),
        level=settings.log.level,
        format="{time:YYYY-MM-DDTHH:mm:ss} | <level>{level}</level> | {extra[user]} | {name}:{function}:{line} | {message}",
        rotation="1 week",
        retention="4 weeks",
    )

    # Set loguru as the handler for the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.log.level)

    # Remove handlers from all the existing loggers and make them propagate to root
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
