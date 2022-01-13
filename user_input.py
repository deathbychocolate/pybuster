import sys

starting_out = """
Please make sure you have all the necessary parameters: [url/uri, wordlist]
"""

documentation_help = """
If you see this it means that you have selected the help option.
This project is currently under construction.
Please, be patient while I make this project better
    
[program name] [-h,--help] -> show the help table
[program name] [-t,--thread] [number] -> select the number of threads to use (default is 10)
[program name] [-w,--wordlist] filename -> select the wordlist you want
"""


def handle_user_input():
    parameters = {}
    arguments = sys.argv[1:]
    if len(arguments) <= 1:
        print(starting_out)
        exit(0)
    elif '-h' in arguments or '--help' in arguments:
        print(documentation_help)
        print(arguments)
        exit(0)
    else:
        # parse user input into dictionary
        while len(arguments) > 0:
            print(arguments)
            parameters[arguments[0]] = arguments[1]
            arguments = arguments[2:]
        print(parameters)
        exit(0)


class UserInput:

    def __init__(self):
        pass

    # Handle all the user parameters - Accept use input and return list of parameters
