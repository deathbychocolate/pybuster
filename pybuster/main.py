"""Demo module"""

import logging

from pybuster.src.command_line_parser import CommandLine
from pybuster.src.pb import _run_pybuster


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Start here"""
    args = CommandLine().run()
    _run_pybuster(args)


if __name__ == "__main__":
    main()
