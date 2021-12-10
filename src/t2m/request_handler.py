import requests
from .yaml_validator import yaml_default, base_url
import os

#JSON constructor for request
def construct_json(protocol, path, param, data):
    #Checking if the values entered are valid
    user, request, _ = yaml_default()
    if not param is None:
        for keys in list(param.keys()):
            if keys in list(request[path][protocol].keys()):
                try:
                    param[keys] = eval(type(request[path][protocol][keys]).__name__)(param[keys])

                except:
                    print(f"Invalid value entered for {keys}. Expected {type(request[path][protocol][keys]).__name__}, got {param[keys]}.")
                    os._exit(1)

    if not data is None:
        for keys in list(data.keys()):
            if keys in list(request[path][protocol].keys()):
                try:
                    data[keys] = eval(type(request[path][protocol][keys]).__name__)(data[keys])

                except:
                    print(f"Invalid value entered for {keys}. Expected {type(request[path][protocol][keys]).__name__}, got {data[keys]}.")
                    os._exit(1)

    return param, data


def set_dry(dry_run = False):
    global dry
    dry = dry_run


def link_builder(path):
    # A simple link builder. combines base_url with directories
    return  base_url() + "/" + path

#There is no use for 'data' in get and delete but to avoid extra positional args, we still pass it as a parameter.
def get(url, param, data):
    return requests.get(url, params = param)

def post(url, param, data):
    return requests.post(url, data = data, params = param)

def patch(url, param, data):
    return requests.patch(url, data = data, params = param)

def delete(url, param, data):
    return requests.delete(url, params = param)


#A request method that has a dry-run feature
#
def request(protocol, path = None, param = None, data = None):
    if path == "token/login":
        login = True
        path = path.split("/")[0]
    else:
        login = False

    p, d = construct_json(protocol, path, param, data)

    global dry
    if dry:
        print(f"Params: {p}")
        print(f"JSON: {d}")
        os._exit(1)

    try:
        response = globals()[protocol](link_builder(path), p, d).json()
        if not response["code"]:
            for keys, values in response.items():
                if keys == "planner":
                    for pkeys, values in response[keys].items():
                        print(f"\033[1;36;1m{pkeys}:\033[0m {values}")
                else:
                    print(f"\033[1;36;1m{keys}:\033[0m {values}")

            if path == "planner" or path == "planners":
                return response

            if path == "user":
                return response

            if path == "token" and login:
                return response["userId"], response["token"]

            return True

        else:
            print(f"\033[31mSomething went wrong.")
            print(f"Error code: {response['code']}")
            print(f"{response['message']}\033[0m")

            return False

    except Exception as err:
        print(f"Request failed! \nError: {err}")
        return False


