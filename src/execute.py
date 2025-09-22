import sys
from importer import Importer


def main():
    Importer.run(sys.argv[1:])
