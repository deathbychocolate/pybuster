"""Pybuster file contains all functions needed to bust a target
"""
import argparse
import concurrent.futures
import sys
import requests


DEFAULT_THREAD_COUNT = 10


def index_file(filename):
    """Index file given filename
    """
    file = open(filename, encoding="latin-1")
    content = {}
    line_count = 1
    for line in file.readlines():
        content[line_count] = line.rstrip()
        line_count = line_count + 1
    data = (content, line_count)

    file.close()
    return data


def assign_per_thread_work(line_count, thread_count):
    """Return a tuple containing the lines_per_thread, lines_per_thread_last
    """
    # Compute the work for each thread
    lines_per_thread = int(line_count / thread_count)

    # Compute how many lines to add to last thread
    lines_to_add = (line_count - (lines_per_thread * thread_count))
    lines_per_thread_last = lines_per_thread + lines_to_add

    return lines_per_thread, lines_per_thread_last


def assign_indexes(data, thread_count):
    """Return a list of tuples (startIndex, endIndex) for each thread
    """
    _, line_count = data
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
    count = start_index

    while count <= end_index:
        url = f"https://dvwa.co.uk/{content[count]}"
        response = requests.get(url, timeout=10, allow_redirects=False)
        if response.status_code != 404:
            print(f"GET {response.status_code} {url}")
        count = count + 1


def handle_user_input():
    """This method uses argparse to process user input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url"     , help="Target Website/URL/URI to enumerate", type=str)
    parser.add_argument("-w", "--wordlist", help="Wordlist to use", type=str)
    parser.add_argument("-t", "--thread"  , help="Number of threads : Default is 10", type=int)
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
        arguments.thread = DEFAULT_THREAD_COUNT

    return arguments


def run(args):
    """Central point to run a job"""
    data = index_file(args.wordlist)
    thread_count = args.thread

    file_thread_indexes = assign_indexes(data, thread_count)
    with concurrent.futures.ThreadPoolExecutor(
            thread_count) as executor:
        for i in range(thread_count):
            args = (data, file_thread_indexes[i])
            executor.submit(perform_http_get_request, args)


def main():
    """Start here"""
    args = handle_user_input()
    run(args)


if __name__ == '__main__':
    main()
