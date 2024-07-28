"""This file contains the configuration for argparse."""

import logging
import sys
import argparse

from pybuster._version import __version__


class CommandLine:
    """Holds all the relevant methods for command line argument parsing using argparse."""

    def __init__(self) -> None:
        pass

    def _parse_user_input(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-u",
            "--url",
            help="Target Website/URL/URI to enumerate.",
            type=str,
        )
        parser.add_argument(
            "-w",
            "--wordlist",
            help="Wordlist to use.",
            type=str,
        )
        parser.add_argument(
            "-t",
            "--threads",
            default=10,
            help="Number of threads [default=10].",
            type=int,
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=__version__,
            help="Print the version number and exit.",
        )
        arguments = parser.parse_args()

        # if arguments.version is not None:
        #     print(__version__)
        #     sys.exit(0)

        # # manual argument check (major)
        # if arguments.url is None:
        #     logging.critical("missing argument 'url'")
        #     parser.print_help()
        #     sys.exit(1)
        # elif arguments.wordlist is None:
        #     logging.critical("missing argument 'wordlist'")
        #     parser.print_help()
        #     sys.exit(1)

        # # manual argument check (minor)
        # if not validators.url(arguments.url):
        #     logging.critical("url parameter is not valid")
        #     logging.critical("make sure to include the protocol (http[s]://)")
        #     sys.exit(1)
        # if not arguments.url.endswith(URL_FORMAT_BACKSLASH):
        #     arguments.url = "".join([arguments.url, URL_FORMAT_BACKSLASH])

        # # set default values
        # if arguments.threads is None:
        #     arguments.threads = THREAD_COUNT_DEFAULT

        return arguments

    def run(self) -> argparse.Namespace:
        """_summary_

        Returns:
            argparse.Namespace: _description_
        """
        args = self._parse_user_input()
        return args
