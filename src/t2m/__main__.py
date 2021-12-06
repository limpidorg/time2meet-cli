import os
import argparse
import sys
import yaml

from t2m import planner

yaml_dirr = str()
yaml_files = dict()
base_url = str()




#Basic JSON constructor.
#Takes its parameters from CLI args, then checks it if they are valid.
#
def construct_json(protocol, path, data, y):
    #Finding the validator.
    y = y['r_settings'][f'{path}'][f'{protocol}']
    if not data:
        print("Your --data should have the following values in the same order:")
        for key in y:
            print(f"{key}")

        print(f"You've entered: {data}")
        quit()

    rjson = {}

    y_keys = list(y.keys())
    y_values = list(y.values())

    # ISSUE: Updating the user config messes up the order of other files in app.yaml. This is a simple workaround and should be investigated more deeply.

    y_keys.reverse()
    y_values.reverse()

    #Checking if the data is valid.
    for i in range(len(data)):
        if  type(y_values[i]) != type(data[i]):
            try:
                data[i] = eval(type(y_values[i]).__name__)(data[i])
            except:
                print(f"Invalid value entered for {y_keys[i]}. Expected {type(y_values[i]).__name__}, got {type(data[i]).__name__}")
                quit()

    #Constructing the JSON.
    for i in range(len(data)):
        rjson[y_keys[i]] = data[i]

    return rjson



def main(args=None):
    #The main routine.
    if args is None:
        args = sys.argv[1:]

    #Init parser
    request_parser = argparse.ArgumentParser()


    request_parser.add_argument(
        "protocol", nargs = "?", default = "none", 
        help = """protocol -> string \n
            [GET, POST, PATCH, DELETE]"""
        )

    request_parser.add_argument(
        "path", nargs = "?", default = "none",
        help = """path -> string \n
                Enter your desired path to send request to."""
        )

    request_parser.add_argument(
            "--updateconfig", nargs = 2,
            help = """Update user_settings in app.yaml"""
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
    update = args.updateconfig



    if update:
        yaml_manage(True, update[0], update[1])
    else:
        yaml_manage()
        globals()[path](protocol, yaml_files["app_settings"]["base_url"], path, construct_json(protocol, path, data, yaml_files))




if __name__ == "__main__":
    sys.exit(main())



