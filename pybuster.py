"""Pybuster file contains all functions needed to bust a target
"""
from concurrent.futures import ThreadPoolExecutor

import argparse
import sys
import requests
import validators

from constants import THREAD_COUNT_DEFAULT
from constants import STATUS_CODES_POSITIVE
from constants import URL_FORMAT_BACKSLASH
from constants import VERSION_NUMBER


def count_lines(filepath: str) -> int:
    """Simply count lines in file
    """
    line_count = 0
    with open(filepath, "rb") as filepointer:
        line_count = len(filepointer.readlines())
    return line_count


def index_file(filename: str) -> dict:
    """Index file given filename
    """
    with open(filename, "rb") as filepointer:
        indexed_wordlist = {}
        line_count = 1
        for line in filepointer.readlines():
            indexed_wordlist[line_count] = line.rstrip()
            line_count = line_count + 1

    return indexed_wordlist


def assign_per_thread_work(line_count: int, thread_count: int) -> tuple[int, int]:
    """Return a tuple containing the lines_per_thread, lines_per_thread_last
    """
    lines_per_thread = int(line_count / thread_count)
    lines_per_thread_last = lines_per_thread + (line_count % thread_count)

    return lines_per_thread, lines_per_thread_last


def assign_indexes(filename: str, thread_count: int) -> list:
    """Return a list of tuples (startIndex, endIndex) for each thread
    """
    line_count = count_lines(filename)
    start_index = 0
    end_index = 0

    file_thread_indexes = []
    count = 1  # start at 1 so that we treat the last thread differently
    lines_per_thread, lines_per_thread_last = assign_per_thread_work(
        line_count, thread_count)

    while count < thread_count:
        start_index = start_index + 1
        end_index = end_index + lines_per_thread
        file_thread_indexes.append((start_index, end_index))
        start_index = end_index
        count = count + 1

    # treat the last thread differently
    start_index = end_index + 1
    end_index = end_index + lines_per_thread_last
    file_thread_indexes.append((start_index, end_index))

    return file_thread_indexes


def http_get(http_get_parameters):
    """Perform simple GET request using requests module
    """
    indexed_wordlist, wordlist_indexes, target_webpage = http_get_parameters
    target_webpage = bytes(target_webpage, 'utf8')
    start_index, end_index = wordlist_indexes

    while start_index <= end_index:
        target_directory = indexed_wordlist[start_index]
        target_full = b''.join([target_webpage, target_directory])
        response = requests.get(target_full, timeout=10, allow_redirects=False)
        if response.status_code in STATUS_CODES_POSITIVE:
            print(f"GET {response.status_code} {target_full.decode()}")
        start_index = start_index + 1


def handle_user_input() -> argparse.Namespace:
    """This method uses argparse to process user input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url"     , help="Target Website/URL/URI to enumerate", type=str)
    parser.add_argument("-w", "--wordlist", help="Wordlist to use"                    , type=str)
    parser.add_argument("-t", "--threads" , help="Number of threads [default=10]"     , type=int)
    parser.add_argument("-v", "--version" , help="Show program version")
    arguments = parser.parse_args()

    if arguments.version is not None:
        print(VERSION_NUMBER)
        sys.exit(0)

    # manual argument check (major)
    if arguments.url is None:
        print("ERROR: missing argument 'url'")
        parser.print_help()
        sys.exit(0)
    elif arguments.wordlist is None:
        print("ERROR: missing argument 'wordlist'")
        parser.print_help()
        sys.exit(0)

    # manual argument check (minor)
    if not validators.url(arguments.url):
        print("ERROR: url parameter is not valid")
        print("ERROR: make sure to include the protocol (http[s]://)")
        sys.exit(0)
    if not arguments.url.endswith(URL_FORMAT_BACKSLASH):
        arguments.url = ''.join([arguments.url, URL_FORMAT_BACKSLASH])

    # set default values
    if arguments.threads is None:
        arguments.threads = THREAD_COUNT_DEFAULT

    return arguments


def run(args: argparse.Namespace) -> None:
    """Central point to run a job
    """
    wordlist_indexed = index_file(args.wordlist)

    file_thread_indexes = assign_indexes(args.wordlist, args.threads)
    with ThreadPoolExecutor(args.threads) as executor:
        for i in range(args.threads):
            http_get_parameters = (wordlist_indexed, file_thread_indexes[i], args.url)
            executor.submit(http_get, http_get_parameters)


def main() -> None:
    """Start here
    """
    args = handle_user_input()
    run(args)


if __name__ == '__main__':
    main()
