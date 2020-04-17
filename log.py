
import logging

def get_log(name):
    FORMAT = '%(asctime)s - %(lineno)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)

    M = 1024 * 1024 * 1024

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(
        f'logs/{name}.log', mode='a', maxBytes=10*M, backupCount=3, encoding='utf-8', delay=0)
    formatter = logging.Formatter(FORMAT)

    handler.setFormatter(formatter)

    log.addHandler(handler)
    return log
