from logging import Formatter, StreamHandler
from logging import CRITICAL, DEBUG, INFO, ERROR, WARNING
from logging import addLevelName, getLevelName, getLogger

def setup_logger(loggername=None, loglevel=INFO):
    formatter = Formatter('[%(levelname)s] %(asctime)s - %(message)s')

    _loggername = loggername if loggername else __name__
    logger = getLogger(loggername)

    addLevelName(CRITICAL, "\033[1;41m%s\033[1;0m" % getLevelName(CRITICAL))
    addLevelName(INFO , "\033[1;32m%s\033[1;0m" % getLevelName(INFO))
    addLevelName(DEBUG, "\033[1;37m%s\033[1;0m" % getLevelName(DEBUG))
    addLevelName(WARNING, "\033[1;33m%s\033[1;0m" % getLevelName(WARNING))
    addLevelName(ERROR, "\033[1;41m%s\033[1;0m" % getLevelName(ERROR))

    if logger.hasHandlers(): return logger

    handler = StreamHandler()
    handler.setLevel(loglevel)
    handler.setFormatter(formatter)
    logger.setLevel(loglevel)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
