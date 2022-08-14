"""Pybuster file contains all functions needed to bust a target
"""
from concurrent.futures import ThreadPoolExecutor

import argparse
import sys
import requests


THREAD_COUNT_DEFAULT  = 10
STATUS_CODES_POSITIVE = [200, 204, 301, 302, 307, 401, 403]
STATUS_CODES_NEGATIVE = [404]


def count_lines(filepath: str) -> int:
    """Simply count lines in file
    """
    linecount = 0
    with open(filepath, "rb") as filepointer:
        linecount = len(filepointer.readlines())
    return linecount


def index_file(filename: str) -> tuple[dict, int]:
    """Index file given filename
    """
    with open(filename, "rb") as filepointer:
        content = {}
        line_count = 1
        for line in filepointer.readlines():
            content[line_count] = line.rstrip()
            line_count = line_count + 1
        data = (content, line_count)

    return data


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


def perform_http_get_request(parameters):
    """Perform simple GET request using requests module
    """
    data, file_thread_indexes = parameters
    content, _ = data
    start_index, end_index = file_thread_indexes

    while start_index <= end_index:
        url = b"https://dvwa.co.uk/" + content[start_index]
        response = requests.get(url, timeout=10, allow_redirects=False)
        if response.status_code in STATUS_CODES_POSITIVE:
            print(f"GET {response.status_code} {url}")
        start_index = start_index + 1


def handle_user_input() -> argparse.Namespace:
    """This method uses argparse to process user input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url"     , help="Target Website/URL/URI to enumerate", type=str)
    parser.add_argument("-w", "--wordlist", help="Wordlist to use"                    , type=str)
    parser.add_argument("-t", "--thread"  , help="Number of threads [default=10]"     , type=int)
    parser.add_argument("-v", "--version" , help="Show program version")
    arguments = parser.parse_args()

    # manual argument check
    if arguments.url is None:
        print("ERROR: missing argument 'url'")
        parser.print_help()
        sys.exit(0)
    elif arguments.wordlist is None:
        print("ERROR: missing argument 'wordlist'")
        parser.print_help()
        sys.exit(0)

    # set default values
    if arguments.thread is None:
        arguments.thread = THREAD_COUNT_DEFAULT

    return arguments


def run(args: argparse.Namespace) -> None:
    """Central point to run a job"""
    data = index_file(args.wordlist)
    thread_count = args.thread

    file_thread_indexes = assign_indexes(args.wordlist, thread_count)
    with ThreadPoolExecutor(thread_count) as executor:
        for i in range(thread_count):
            args = (data, file_thread_indexes[i])
            executor.submit(perform_http_get_request, args)


def main() -> None:
    """Start here"""
    args = handle_user_input()
    run(args)


if __name__ == '__main__':
    main()
