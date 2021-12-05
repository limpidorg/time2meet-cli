import os
import argparse
import sys
import yaml

from t2m import planner

yaml_dirr = str()
yaml_files = dict()

base_url = str()


#Simple yaml manager to read and update app.yaml
#
def yaml_manage(update = False, update_key = None, update_value = None):

    #Use global directory and file.
    global yaml_dirr, yaml_files

    #Finding app.yaml.
    yaml_dirr = os.getcwd()+ "/t2m/usrconf/app.yaml"
    yaml_files = {}


    #Parsing and checking the validation of the yaml file.
    with open(yaml_dirr, "r") as f:
        confirm_yaml = 0
        yf = list(yaml.load_all(f, Loader=yaml.FullLoader))
        for files in yf:
            try:
                yaml_files['app_settings'] = files["app_settings"]
                confirm_yaml += 1

            except:
                try:
                    yaml_files['user_settings'] = files["user_settings"]
                    confirm_yaml += 1

                except:
                    yaml_files['r_settings'] = files["r_settings"]
                    confirm_yaml += 1

        if confirm_yaml != 3:
            print(f"YAML file broken. Check {yaml_dirr}.")
            quit()


    if not update:
        return


        
    #Creating a copy and modifiying said copy to then dump into app.yaml to update it.
    for files in yf:
        if list(files.keys())[0] == "user_settings":
            if  type(files["user_settings"][update_key]) != type(update_value):
                try:
                    update_value = eval(type(files["user_settings"][update_key]).__name__)(update_value)
                except:
                    print(f"""Invalid value entered for {files['user_settings'][update_key]}.
                            Expected {type(files['user_settings'][update_key]).__name__}, got {type(update_value).__name}.""")
                    quit()
            files["user_settings"][update_key] = update_value
            break


    with open(yaml_dirr, "w") as f:
        yaml.dump_all(yf, f, default_flow_style = False)
        print("Updated user settings.")





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


    # TODO: Create other handlers and get their values from args to then use globals() to treat it as a method 
    # TODO: Using a yaml file, define what to use in the JSON for different protocols.

    if update:
        yaml_manage(True, update[0], update[1])
    else:
        yaml_manage()
        globals()[path](protocol, yaml_files["app_settings"]["base_url"], path, construct_json(protocol, path, data, yaml_files))


    #planner_handler.py ->
    #planner(protocol, base_url, path, data)


if __name__ == "__main__":
    sys.exit(main())



