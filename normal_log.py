import logging


def set_loglevel(level, log_file='app.log'):
    try:
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s : %(filename)s : %(lineno)d - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(f"./.logs/{log_file}")
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
