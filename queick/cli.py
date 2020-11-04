import sys
import argparse
from logging import DEBUG, INFO, getLogger

from .worker import Worker
from .logger import setup_logger

logger = getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Queick')
    parser.add_argument('--ping-host')
    parser.add_argument('--ping-port')
    parser.add_argument('-debug', action='store_true')
    parser.add_argument('--log-filepath')
    args = parser.parse_args()

    loglevel = DEBUG if args.debug else INFO
    setup_logger(loglevel=loglevel, filepath=args.log_filepath)
    logger.info('Welcome to Queick!')
    sys.path.append('.')
    w = Worker()
    w.work(args)
