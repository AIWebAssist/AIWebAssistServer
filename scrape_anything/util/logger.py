import logging
import sys
import os
import shutil

LOGGING_FILE = "outputs/logging.log"


def build_logger():
    """create the logger instance"""
    # Define logger
    logger = logging.getLogger("Logger")

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)  # set logger level
        log_formatter = logging.Formatter(
            "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"
        )
        console_handler = logging.StreamHandler(
            sys.stdout
        )  # set streamhandler to stdout
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)
        
        log_dir = os.path.dirname(LOGGING_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(LOGGING_FILE)
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

    return logger


class Logger:
    """a static logger class to share will all components"""

    enabled = True
    logger = build_logger()

    @classmethod
    def change_logging_status(cls, new_status):
        """enable or disable status"""
        cls.enabled = new_status

    @classmethod
    def info(cls, msg, *args, **kwargs):
        """log info"""
        if cls.enabled:
            cls.logger.info(msg, *args, **kwargs)

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        """log error"""
        if cls.enabled:
            cls.logger.debug(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        """log error"""
        if cls.enabled:
            cls.logger.error(msg, *args, **kwargs)

    @classmethod
    def error_execption(cls, _):
        """log execption"""
        if cls.enabled:
            cls.logger.error(
                "got an execption:",
                exc_info=sys.exc_info(),
            )

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        """log warning"""
        if cls.enabled:
            cls.logger.warning(msg, *args, **kwargs)

    @classmethod
    def copy_log_file(cls, uuid):
        logging.shutdown()

        if not os.path.exists("outputs/logs"):
            os.makedirs("outputs/logs")

        shutil.copy(
            LOGGING_FILE, os.path.join("outputs", "logs", f"{uuid}_experiment.log")
        )
        os.remove(LOGGING_FILE)
        Logger.logger = build_logger()
