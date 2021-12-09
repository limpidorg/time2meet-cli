import os
import argparse
import sys

from t2m import user, planner, tokens, update_password

from .planner import *
from .user import *
from .tokens import *
from .update_password import *
from .request_handler import set_dry


#Simple error printer
#
def print_err(err, success, pars, varn):
    if success:
        print()
        for m in err: 
            print(f"\033[1;36;1m{m} \033[0m")
            print()

    else:
        print()
        print(f"\033[31m{varn}: \033[0m \033[1;36;1m'{err}'\033[0m \033[31mdoes not exist.\033[0m")
        print()

    print(pars.format_help())
    os._exit(1)


# A way to list all methods of a path
#
def list_methods(path):
    return dir(path)

#The main routine
#
def main(args=None):
    if args is None:
        args = sys.argv[1:]

    #Init parser
    request_parser = argparse.ArgumentParser(prog = "t2m", add_help = False)

    request_parser.add_argument(
            "path", nargs = "?", action="store", default = None,
            help = """path -> string \n
                Enter your desired path to send request to.\n
                [planner, user, token, update_password]"""
                )

    request_parser.add_argument(
            "method", nargs = "?", action="store", default = None,
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

    request_parser.add_argument(
            "-d", "--dry", action="store_true",
            help = "Print out the parameters and the data that you will send without sending the request."
            )

    #Parsing our arguments
    args = request_parser.parse_args()
    path = args.path
    method = args.method
    params = args.params

    #Set the dry-run feature
    set_dry(args.dry)

    #Create a list available endpoints
    paths = ["planner", "tokens", "user", "update_password"]

    if not path:
        print("\033[33mAvailable paths:\033[0m")
        print_err(paths, True, request_parser, "Path")

    elif path not in paths:
        print_err(path, False, request_parser, "Path")

    try:
        path = args.path.lower()

    except:
        print(request_parser.format_help())
        os._exit(1)

    #Create a list of available methods
    methods = list_methods(globals()[path])

    #Show available methods
    if not method or method not in methods:
        try:
            print("\033[33mAvailable methods for {path}:\033[0m")
            print_err(methods, True, request_parser, "Method")
            
        except:
            print_err(path, False, request_parser, "Path")

    #Create a list of available methods
    param = globals()[method].__code__.co_varnames[:globals()[method].__code__.co_argcount]

    #Show required parameters
    if not params and param:
        try:
            print(f"\033[33mParameters required for {method}:\033[0m")
            print_err(param, True, request_parser, "Param")

        except:
            print_err(method, False, request_parser, "Method")

    if param:
        globals()[method](params)
    else:
        globals()[method]()

if __name__ == "__main__":
    sys.exit(main())


