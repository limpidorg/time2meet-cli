import requests
import json


def link_builder(base_url, directories) -> str:
    """ A simple link builder. combines base_url with directories"""
    return base_url + "/".join(directories)

# TODO: Setup user authentication system

def get(url):
    return requests.get(url)

def post(url, data):
    return requests.post(url, data = data)

def put(url, data):
    return requests.put(url, data = data)

def post(url, data):
    return requests.post(url, data = data)

def delete(url):
    return requests.delete(url)


def request(protocol, url, data = None):
    try:
        response = globals()[protocol](url, data)
    
    except Exception as err:
        print(f"Request failed! \n Error: {err}")

    else:
        return response.json()
