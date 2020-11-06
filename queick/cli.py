import sys
import argparse
from logging import DEBUG, INFO, getLogger

from .worker import Worker
from .logger import setup_logger

logger = getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Queick')
    parser.add_argument('-ph', '--ping-host', help='hostname for NetworkWatcher to check if the machine has the internet connection')
    parser.add_argument('-pp', '--ping-port', help='port number for NetworkWatcher')
    parser.add_argument('-debug', help='if set, detailed logs will be shown', action='store_true')
    parser.add_argument('-lf', '--log-filepath', help='logfile to save all the worker log')
    args = parser.parse_args()

    loglevel = DEBUG if args.debug else INFO
    setup_logger(loglevel=loglevel, filepath=args.log_filepath)
    logger.info('Welcome to Queick!')
    sys.path.append('.')
    w = Worker()
    w.work(args)
