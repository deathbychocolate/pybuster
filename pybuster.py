#!/bin/python3
import concurrent.futures

import requests

from user_input import handle_user_input


def index_file(filename):
    file = open(filename, encoding="latin-1")
    content = {}
    line_count = 1
    for line in file.readlines():
        content[line_count] = line.rstrip()
        line_count = line_count + 1
    data = (content, line_count)

    file.close()
    return data


# Return a tuple containing the lines_per_thread, lines_per_thread_last
def assign_per_thread_work(line_count, thread_count):
    # Compute the work for each thread
    lines_per_thread = int(line_count / thread_count)

    # Compute how many lines to add to last thread
    lines_to_add = (line_count - (lines_per_thread * thread_count))
    lines_per_thread_last = lines_per_thread + lines_to_add

    return lines_per_thread, lines_per_thread_last


# Return a list of tuples (startIndex, endIndex) for each thread
def assign_indexes(data, thread_count):
    file_content, line_count = data
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
    # indexing for last thread
    start_index = end_index + 1
    end_index = end_index + lines_per_thread_last
    file_thread_indexes.append((start_index, end_index))

    return file_thread_indexes


# Thread function
def perform_http_get_request(parameters):
    data, file_thread_indexes = parameters
    content, line_count = data
    start_index, end_index = file_thread_indexes
    count = start_index
    while count <= end_index:
        url = f"https://dvwa.co.uk/{content[count]}"
        r = requests.get(url, timeout=10, allow_redirects=False)
        if r.status_code != 404:
            print(f"GET {r.status_code} {url}")
        count = count + 1


def run():
    parameters = handle_user_input()
    data = index_file(parameters["--wordlist"])
    thread_count = parameters["--thread"]

    file_thread_indexes = assign_indexes(data, thread_count)
    with concurrent.futures.ThreadPoolExecutor(
            thread_count) as executor:
        for i in range(thread_count):
            parameters = (data, file_thread_indexes[i])
            executor.submit(perform_http_get_request, parameters)
