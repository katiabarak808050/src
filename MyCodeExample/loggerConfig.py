import logging


def set_file_logger(name: str, log_file_name: str) -> logging.Logger:
    """
    logging configuration
    log record example: 2021-04-12 22:31:58,799 | ERROR | Message1
    :param name: logger name, usually a module name (__name__)
    :param log_file_name: log file path
    :return: named logger object

    """
    logger = logging.getLogger(name)

    # set log level
    logger.setLevel(logging.WARNING)

    # define file handler and set formatter
    file_handler = logging.FileHandler(log_file_name)
    # format configuration: 2022-07-16 22:31:58,799 | ERROR | Message
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)
    return logger
