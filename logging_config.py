# logging_config.py

import logging
from logging.handlers import RotatingFileHandler

def configure_logger(file_path):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(file_path, maxBytes=100000, backupCount=1)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
