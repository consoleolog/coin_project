import logging
import time


def log_setting(status):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    log_file_name = time.strftime("%Y-%M-%D_%H:%M:%S", time.localtime(time.time()))

    logger = logging.getLogger()

    if status == "INFO":
        logger.setLevel(logging.INFO)
    if status == "ERROR":
        logger.setLevel(logging.ERROR)
    if status == "WARN":
        logger.setLevel(logging.WARN)

    formatter = logging.Formatter(f"[%(levelname)s] {current_time} :: %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(f".logs/my.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


log_info = log_setting("INFO")

log_error = log_setting("ERROR")

log_warn = log_setting("WARN")
