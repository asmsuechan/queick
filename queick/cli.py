import argparse

from .worker import Worker


def main():
    parser = argparse.ArgumentParser(description='Queick')
    parser.add_argument(
        '-ph',
        '--ping-host',
        help='hostname for NetworkWatcher to check if the machine has the internet connection')
    parser.add_argument('-pp', '--ping-port',
                        help='port number for NetworkWatcher')
    parser.add_argument(
        '-debug',
        help='if set, detailed logs will be shown',
        action='store_true')
    parser.add_argument('-lf', '--log-filepath',
                        help='logfile to save all the worker log')
    args = parser.parse_args()

    w = Worker()
    w.work(
        ping_host=args.ping_host,
        ping_port=args.ping_port,
        debug=args.debug)
