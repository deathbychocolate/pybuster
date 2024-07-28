"""
Pybuster file contains all functions needed to bust a target
"""
import argparse
import logging
import sys
from concurrent.futures import ThreadPoolExecutor

import requests
import validators

from pybuster.src.constants import STATUS_CODES_POSITIVE, THREAD_COUNT_DEFAULT, URL_FORMAT_BACKSLASH, VERSION_NUMBER


def _run_pybuster(args: argparse.Namespace) -> None:
    wordlist_indexed = _index_the_file(args.wordlist)
    file_thread_indexes = _assign_indexes(args.wordlist, args.threads)
    with ThreadPoolExecutor(args.threads) as executor:
        for i in range(args.threads):
            http_get_parameters = (wordlist_indexed, file_thread_indexes[i], args.url)
            executor.submit(_http_get, http_get_parameters)


def _assign_indexes(filepath: str, thread_count: int) -> list:
    line_count = _count_lines_in_file(filepath)
    start_index = 0
    end_index = 0

    file_thread_indexes = []
    count = 1  # start at 1 so that we treat the last thread differently
    lines_per_thread, lines_per_thread_last = _assign_work_to_each_thread(
        line_count, thread_count
    )

    logging.info("assigning indexes to each thread...")
    while count < thread_count:
        logging.info("thread %s...", count)
        start_index = start_index + 1
        end_index = end_index + lines_per_thread
        file_thread_indexes.append((start_index, end_index))
        start_index = end_index
        count = count + 1

    logging.info("assigning our calculated average to the last thread + remainder")
    start_index = end_index + 1
    end_index = end_index + lines_per_thread_last
    file_thread_indexes.append((start_index, end_index))

    return file_thread_indexes


def _count_lines_in_file(filepath: str) -> int:
    line_count = 0
    with open(filepath, "rb") as filepointer:
        logging.info("counting the lines in '%s'...", {filepath})
        line_count = len(filepointer.readlines())
        logging.info("completed the lines in '%s'...", {filepath})
    return line_count


def _index_the_file(filepath: str) -> dict:
    with open(filepath, "rb") as filepointer:
        logging.info("Opened '%s' successfully...", filepath)
        indexed_wordlist = {}
        line_count = 1
        for line in filepointer.readlines():
            indexed_wordlist[line_count] = line.rstrip()
            line_count = line_count + 1
        logging.info("completed indexing of '%s'...", filepath)

    if len(indexed_wordlist) == 0:
        logging.critical("The wordlist seems to be empty...")
        raise ValueError("The wordlist seems to be empty...")

    return indexed_wordlist


def _assign_work_to_each_thread(line_count: int, thread_count: int) -> tuple[int, int]:
    logging.info("assigning number of lines per thread...")
    lines_per_thread = int(line_count / thread_count)
    lines_per_thread_last = lines_per_thread + (line_count % thread_count)
    logging.info("completed assigning number of lines per thread...")
    return lines_per_thread, lines_per_thread_last


def _http_get(http_get_parameters):
    indexed_wordlist, wordlist_indexes, target_webpage = http_get_parameters
    target_webpage = bytes(target_webpage, "utf8")
    start_index, end_index = wordlist_indexes

    while start_index <= end_index:
        target_directory = indexed_wordlist[start_index]
        target_full = b"".join([target_webpage, target_directory])
        response = requests.get(target_full, timeout=10, allow_redirects=False)
        if response.status_code in STATUS_CODES_POSITIVE:
            print(f"GET {response.status_code} {target_full.decode()}")
        start_index = start_index + 1
