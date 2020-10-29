from .worker import Worker
import sys

def main():
    sys.path.append('.')
    w = Worker()
    w.work()
