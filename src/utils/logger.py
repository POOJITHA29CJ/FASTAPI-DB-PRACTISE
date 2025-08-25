import logging
import os
def setup_logger():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logger=logging.getLogger("app_logger")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh=logging.FileHandler("logs/app.log")
        formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter) 
        logger.addHandler(fh)
    return logger


