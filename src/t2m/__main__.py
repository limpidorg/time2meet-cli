import os
import argparse
import sys

import planner
import user
import request_handler as rh

from planner import *
from user import *

yaml_dirr = str()
yaml_files = dict()
base_url = str()




# A way to list all methods of a path
#
def list_methods(path):
    return dir(path)

#The main routine.
#
def main(args=None):
    if args is None:
        args = sys.argv[1:]

    #Init parser
    request_parser = argparse.ArgumentParser(prog = "t2m", add_help = False)

    request_parser.add_argument(
            "path", nargs = "?", default = None,
            help = """path -> string \n
                Enter your desired path to send request to. \n
                [planner, user]"""
                )

    request_parser.add_argument(
            "method", nargs = "?", default = None,
            help = """methods -> string \n
                Enter the method you want to execute for the path."""
                )

    request_parser.add_argument(
            "-p", "--params", nargs = "*", default = None,
            help = """params -> str \n
                Enter the required parameters for methods."""
            )

    request_parser.add_argument(
            "-h", "--help", nargs = "?", action="store",
            help = "Required arguments -> path, method."
            )

    args = request_parser.parse_args()
    params = args.params

    try:
        path = args.path.lower()

    except:
        print(request_parser.format_help())
        os._exit(1)

    method = args.method

    #Show available methods if it's missing
    if not method:
        try:
            methods = list_methods(globals()[path])
            print(f"Avaliable methods for {path}:")

            for m in methods:
                print(f"\033[1;36;1m \033")
                print(m)

            print()

        except:
            print()
            print(f"\033[31mPath:\033 \033[1;36;1m'{path}'\033[0m \033[31mdoes not exist.\033[0m")
            print()
            print(request_parser.format_help())

        os._exit(1)

    if not params:
        try:
            param = globals()[method].__code__.co_varnames[:globals()[method].__code__.co_argcount]
            print(f"Parameters required for {method}:")

            for p in param:
                print(f"\033[1;36;1m \033")
                print(p)

            print()

        except:
            print()
            print(f"\033[31mMethod:\033 \033[1;36;1m'{method}'\033[0m \033[31mdoes not exist.\033[0m")
            print()
            print(request_parser.format_help())

        os._exit(1)



if __name__ == "__main__":
    sys.exit(main())


