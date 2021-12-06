from .request_handler import request



#Basic planner functions using Time2Meet API
def planner(protocol, base_url, path, param = None, data = None):
    response = request(protocol, base_url, path, param = param, data = data)

    if response['code'] < 0:
        print(f"Error: {response['message']}")
        quit()

    print(f"{response['message']}")
    if protocol == "post":
        print(f"Planner ID: {response['plannerId']}")
    else:
        print(response)
