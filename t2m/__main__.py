import os
import argparse
import sys

from t2m import planner


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    base_url = "https://time2meetapis.yyjlincoln.app/"

    #Init parser
    request_parser = argparse.ArgumentParser()

    request_parser.add_argument(
        "protocol", 
        help = """protocol -> string \n
            [GET, POST, PATCH, DELETE]"""
        )

    request_parser.add_argument(
        "path",
        help = """path -> string \n
                Enter your desired path to send request to."""
        )

    request_parser.add_argument(
        "--data", nargs = "*",
        help = """data -> appropiate JSON for specified protocol \n
                See the Docs."""
        )

    args = request_parser.parse_args()

    #parse_args() returns the arguments we created as variables. By default they are all string

    protocol = args.protocol.lower()
    path = args.path
    data = args.data


    # TODO: Create other handlers and get their values from args to then use globals() to treat it as a method 
    # TODO: Using a yaml file, define what to use in the JSON for different protocols.

    #planner_handler.py ->
    planner(protocol, base_url, path, data)


if __name__ == "__main__":
    sys.exit(main())



