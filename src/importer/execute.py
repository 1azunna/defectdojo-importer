import sys
from importer import Importer


def main():
    """Entry point for the DefectDojo Importer CLI."""
    Importer.run(sys.argv[1:])
