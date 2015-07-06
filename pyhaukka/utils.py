import logging
from logging.handlers import RotatingFileHandler

def init_logger(module, log_file='', level=logging.DEBUG):
    # set up logging to file and console
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
    console.setLevel(logging.INFO)

    if not log_file:
        log_file = module + '.log'
    rotating_file = logging.handlers.RotatingFileHandler(filename=log_file)
    rotating_file.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M'))

    logger = logging.getLogger(module)
    logger.setLevel(level)
    logger.addHandler(console)
    logger.addHandler(rotating_file)

    return logger

def dicts_subset_filter(d, subset, ignore_keys=[]):
    '''
    Checks if b is subset of a
    '''
    ka = set(d).difference(ignore_keys)
    kb = set(subset).difference(ignore_keys)
    return kb.issubset(ka) and all(d[k] == subset[k] for k in kb)

