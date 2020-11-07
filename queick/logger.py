from logging import FileHandler, Formatter, StreamHandler
from logging import CRITICAL, DEBUG, INFO, ERROR, WARNING
from logging import addLevelName, basicConfig, getLevelName, getLogger


def setup_logger(loglevel=INFO, filepath=None):
    formatter = Formatter('[%(levelname)s] %(asctime)s - %(message)s')

    logger = getLogger('queick')

    if filepath:
        fileHandler = FileHandler(filepath)
        logFormatter = Formatter("[%(levelname)s] %(asctime)s %(message)s")
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

    addLevelName(CRITICAL, "\033[1;41m%s\033[1;0m" % getLevelName(CRITICAL))
    addLevelName(INFO, "\033[1;32m%s\033[1;0m" % getLevelName(INFO))
    addLevelName(DEBUG, "\033[1;37m%s\033[1;0m" % getLevelName(DEBUG))
    addLevelName(WARNING, "\033[1;33m%s\033[1;0m" % getLevelName(WARNING))
    addLevelName(ERROR, "\033[1;41m%s\033[1;0m" % getLevelName(ERROR))

    handler = StreamHandler()
    handler.setLevel(loglevel)
    handler.setFormatter(formatter)
    logger.setLevel(loglevel)
    logger.addHandler(handler)
    logger.propagate = False
