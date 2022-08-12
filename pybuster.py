"""Pybuster file contains all functions needed to bust a target
"""
import argparse
import concurrent.futures

import requests


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
        r = requests.get(url, timeout=10, allow_redirects=False)
        if r.status_code != 404:
            print(f"GET {r.status_code} {url}")
        count = count + 1


def handle_user_input():
    """This method uses argparse to process user input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("target",           help="Target Website/URL/URI to enumerate")
    parser.add_argument("-t", "--thread",   help="Number of threads : Default is 10")
    parser.add_argument("-w", "--wordlist", help="Wordlist to use   : Default is ./wordlist.txt")
    parser.add_argument("-v", "--version",  help="Show program version")
    arguments = parser.parse_args()

    if arguments.thread is not None:
        arguments.thread = int(arguments.thread)
    # if arguments.url is not None:

    # if arguments.url is not None:

    return arguments


def run(args):
    """Central point to run a job"""
    args = handle_user_input()
    data = index_file(args.wordlist)
    thread_count = args.thread

    file_thread_indexes = assign_indexes(data, thread_count)
    with concurrent.futures.ThreadPoolExecutor(
            thread_count) as executor:
        for i in range(thread_count):
            args = (data, file_thread_indexes[i])
            executor.submit(perform_http_get_request, args)
