import logging, os
from logging.handlers import RotatingFileHandler

def init_loggers(log_file='app.log', level=logging.DEBUG):
    logger = logging.getLogger()

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))

    logger.addHandler(console)

    if os.environ.get('HEROKU') is None:
        console.setLevel(logging.INFO)
        rotating_file = logging.handlers.RotatingFileHandler(filename=log_file)
        rotating_file.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M'))
        logger.addHandler(rotating_file)

    logger.setLevel(level)


def dicts_subset_filter(d, subset, ignore_keys=[]):
    '''
    Checks if b is subset of a
    '''
    ka = set(d).difference(ignore_keys)
    kb = set(subset).difference(ignore_keys)
    return kb.issubset(ka) and all(d[k] == subset[k] for k in kb)

