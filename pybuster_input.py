import sys

project_name = "pybuster"

documentation_help = f"""
    
{project_name} [-h|--help]                  -> show the help table
{project_name} [-t|--thread] [number]       -> select thread number (default is 10)
{project_name} [-w|--wordlist] [filename]   -> select your wordlist
{project_name} [-u|--url] [URL]             -> select the URL to test

Example commands:
{project_name} -h
{project_name} -u "http://www.revil.com:80/" -t 50 -w file.txt
{project_name} --url "http://www.revil.com:80/" --thread 50 --wordlist file.txt

"""

supported_parameters = [
    "-h", "--help",
    "-t", "--thread",
    "-u", "--url",
    "-w", "--wordlist"
]

required_parameter_url = ["-u", "--url"]
required_parameter_wordlist = ["-w", "--wordlist"]


def handle_user_input():
    parameters = {}
    arguments = sys.argv[1:]
    if len(arguments) <= 1:
        print(documentation_help)
        exit(0)
    else:
        arguments.reverse()
        while len(arguments) > 0:
            parameter_name = arguments.pop()
            parameter_value = arguments.pop()
            if '-' in parameter_value and '-' in parameter_value:
                parameters[parameter_name] = ""
                parameters[parameter_value] = ""
            else:
                parameters[parameter_name] = parameter_value
        print(parameters)

        # check that all parameters are supported
        stop = False
        for key in parameters.keys():
            if key not in supported_parameters:
                print(f"Sorry, parameter '{key}' is not supported")
                stop = True
        if stop:
            exit(0)

        # check for required parameter
        for item in required_parameter_url:
            if item not in parameters.keys():
                print("Missing required parameters")
                print("Please, include the [-u|--url] parameter")
        # check for required parameter
        for item in required_parameter_wordlist:
            if item not in parameters.keys():
                print("Missing required parameters")
                print("Please, include the [-w|--wordlist] parameter")

        # convert thread value from string to int
        if "-t" in parameters:
            parameters["-t"] = int(parameters["-t"])
        elif "--thread" in parameters:
            parameters["--thread"] = int(parameters["--thread"])
        else:
            parameters["--thread"] = 10

    return parameters


class UserInput:

    def __init__(self):
        pass
