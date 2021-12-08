import requests
from yaml_validator import yaml_default, base_url
import os

def construct_json(protocol, path, param, data):
    #Checking if the values entered are valid
    user, request = yaml_default()
    for keys in list(param.keys()):
        if keys in list(user[protocol].keys()):
            try:
                param[keys] = eval(type(files[keys]).__name__)(param[keys])

            except:
                print(f"Invalid value entered for {keys}. Expected {type(user[protocol][keys]).__name__}, got {param[keys]}.")
                os._exit(1)

    for keys in list(data.keys()):
        if keys in list(request[protocol].keys()):
            try:
                data[keys] = eval(type(files[keys]).__name__)(data[keys])

            except:
                print(f"Invalid value entered for {keys}. Expected {type(request[protocol][keys]).__name__}, got {data[keys]}.")
                os._exit(1)

    return param, data



def link_builder(path):
    """ A simple link builder. combines base_url with directories"""
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


def request(protocol, path = None, param = None, data = None):
    p, d = construct_json(protocol, path, param, data)

    try:
        response = globals()[protocol](link_builder(path), p, d)

    except Exception as err:
        print(f"Request failed! \nError: {err}")
        quit()

    else:
        return response.json()
