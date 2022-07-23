"""Demo module"""
import pybuster


def main():
    """Start here"""
    args = pybuster.handle_user_input()
    pybuster.run(args)


if __name__ == "__main__":
    main()
