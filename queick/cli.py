from .worker import Worker
from .logger import logger
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Queick')
    parser.add_argument('--ping-host')
    parser.add_argument('--ping-port')
    args = parser.parse_args()

    logger.info('Welcome to Queick!')
    sys.path.append('.')
    w = Worker()
    w.work(args)
