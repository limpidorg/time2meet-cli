from .request_handler import request



#Basic planner functions using Time2Meet API
def planner(protocol, base_url, path, param = None, data = None):
    response = request(protocol, base_url, path, param = None, data = None)

    if response['code'] < 0:
        print(f"Error: {response['message']}")
        quit()

    print(f"{response['message']}")
