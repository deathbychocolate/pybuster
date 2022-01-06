#!/bin/python3
import requests
import concurrent.futures


'''
Return a tuple containing file_content{} and line_count
'''
def process_file(filename):
    file = open(filename, encoding="latin-1")
    content = {}
    line_count = 1
    for line in file.readlines():
        content[line_count] = line.strip()
        line_count = line_count + 1
    data = (content, line_count)

    file.close()
    return data


'''
Return a tuple containing the lines_per_thread, lines_per_thread_last
'''
def assign_per_thread_work(line_count, thread_count):
    # Compute the work for each thread
    lines_per_thread = int( line_count / thread_count )
    
    #Compute how many lines to add to last thread
    lines_to_add = (line_count - (lines_per_thread * thread_count))
    lines_per_thread_last = lines_per_thread + lines_to_add

    return lines_per_thread, lines_per_thread_last


'''
Return a list of tuples that contain (startIndex, endIndex) for each thread
'''
def assign_indeces(data, thread_count):
    file_content, line_count = data
    startIndex = 0
    endIndex = 0
    
    file_thread_indeces = []
    count = 1 # start at 1 so that we treat the last thread differently
    lines_per_thread, lines_per_thread_last = assign_per_thread_work(line_count, thread_count)
    while count < thread_count:
        startIndex = startIndex + 1
        endIndex = endIndex + lines_per_thread
        file_thread_indeces.append((startIndex, endIndex))
        startIndex = endIndex
        count = count + 1
    # indexing for last thread
    startIndex = endIndex + 1
    endIndex = endIndex + lines_per_thread_last
    file_thread_indeces.append((startIndex, endIndex))

    return file_thread_indeces


'''
Thread function
'''
def perform_GET(parameters):
    data, file_thread_indeces = parameters
    content, line_count = data
    startIndex, endIndex = file_thread_indeces
    count = startIndex
    while count <= endIndex:
        url = f"https://dvwa.co.uk/{content[count]}"
        r = requests.get(url, timeout=10, allow_redirects=False)
        scode = r.status_code
        if scode != 404:
            print(f"GET {r.status_code} {url}")
        count = count + 1



if __name__=="__main__":

    filename = "/usr/share/dirb/wordlists/common.txt"
    data = process_file(filename)
    
    content, line_count = data
    thread_count = 10
    
    file_thread_indeces = assign_indeces(data, thread_count)
    with concurrent.futures.ThreadPoolExecutor(thread_count) as executor:
        for i in range(thread_count):
            parameters = (data, file_thread_indeces[i])
            executor.submit(perform_GET, parameters)
