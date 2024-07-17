import logging
import os

fmt = "[%(levelname)s] %(asctime)s : %(filename)s : %(lineno)d - %(message)s"
datefmt = '%Y-%m-%d %H:%M:%S'


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=datefmt)
        return formatter.format(record)


def set_loglevel(level, log_file='app.log'):
    try:
        if not os.path.exists(f"{os.getcwd()}/.logs"):
            os.mkdir(f"{os.getcwd()}/.logs")

        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(CustomFormatter(fmt))

        file_handler = logging.FileHandler(f"{os.getcwd()}/.logs/{log_file}")
        file_handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        if level.upper() == "D":
            logger.setLevel(logging.DEBUG)
        elif level.upper() == "E":
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.INFO)

    except Exception:
        raise
