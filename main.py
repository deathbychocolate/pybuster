"""Demo module"""
import logging
from pybuster import handle_user_input
from pybuster import run


def main():
    """Start here"""
    logging.basicConfig(level=logging.INFO)
    args = handle_user_input()
    run(args)


if __name__ == "__main__":
    main()
