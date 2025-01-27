import logging

def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger with the given name and log file.

    :param name: The name of the logger.
    :param log_file: The file to save logs.
    :param level: The logging level.
    :return: A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
