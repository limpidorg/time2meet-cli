import requests


def link_builder(base_url, directories) -> str:
    """ A simple link builder. combines base_url with directories"""
    return base_url + "/" + directories

# TODO: Setup user authentication system

#There is no use for 'data' in get and delete but to avoid extra positional args, we still pass it as a parameter.
def get(url, param, data):
    return requests.get(url, params = param)

def post(url, param, data):
    return requests.post(url, data = data, params = param)

def patch(url, param, data):
    return requests.patch(url, data = data, params = param)

def delete(url, param, data):
    return requests.delete(url, params = param)


def request(protocol, base_url, path = None, param = None, data = None):
    try:
        response = globals()[protocol](link_builder(base_url, path), param, data)
    
    except Exception as err:
        print(f"Request failed! \nError: {err}")
        quit()

    else:
        return response.json()
