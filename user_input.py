import sys

project_name = "pybuster"

starting_out = f"""
With {project_name} you must include the URL/URI, and the wordlist flags

Example commands:
{project_name} -h
{project_name} -u "http://www.localhost.com:80/" -t 50 -w file.txt
{project_name} --url "http://www.localhost.com:80/" --thread 50 --wordlist file.txt
"""

documentation_help = f"""
This project is currently under construction.
Please, be patient while I make this project better.
    
{project_name} [-h|--help] -> show the help table
{project_name} [-t|--thread] [number] -> select the number of threads to use (default is 10)
{project_name} [-w|--wordlist] filename -> select the wordlist you want
{project_name} [-u|--url] URL -> select the URL you want to test
"""

error_message_parameter = f"{project_name} does not recognise parameter"
error_message_parameter_name = f"{error_message_parameter} name"
error_message_parameter_value = f"{error_message_parameter} value"


def handle_user_input():
    parameters = {}
    arguments = sys.argv[1:]
    if len(arguments) <= 1:
        print(starting_out)
        exit(0)
    elif '-h' in arguments or '--help' in arguments:
        print(documentation_help)
        exit(0)
    else:
        arguments.reverse()
        while len(arguments) > 0:
            parameter_name = arguments.pop()
            parameter_value = arguments.pop()
            if '-' not in parameter_name and '--' not in parameter_name:
                print(
                    f"{error_message_parameter_name} {parameter_name}"
                )
                exit(0)
            parameters[parameter_name] = parameter_value
        print(parameters)

        # check required parameters: -w/--wordlist
        if "-w" not in parameters and "--wordlist" not in parameters:
            print("Missing required parameter -w/--wordlist")
            exit(0)

        # check required parameters: -u/--url
        if "-u" in parameters:
            parameters["-u"] = parameters["-u"]
        elif "--url" in parameters:
            parameters["--url"] = parameters["--url"]
        else:
            print("Missing required parameter -u/--url")
            exit(0)

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
