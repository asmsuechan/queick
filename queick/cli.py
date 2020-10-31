from .worker import Worker
from .logger import logger
import sys

def main():
    logger.info('Welcome to queick!')
    sys.path.append('.')
    w = Worker()
    w.work()
