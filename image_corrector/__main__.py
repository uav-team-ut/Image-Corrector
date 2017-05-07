import sys

from .corrector import Corrector

if __name__ == '__main__':

    Corrector(*sys.argv[1:])
