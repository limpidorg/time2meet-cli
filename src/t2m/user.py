import os
from getpass import getpass
from request_handler import request
from datetime import  datetime, tzinfo
import json

def __dir__():
    return ["user_info", "register", "edit_profile", "delete_profile"]

def user_req(protocol, param = None, data = None):
    response = request(protocol, "user", param = param, data = data)

    if not response["code"]:
        for keys, values in response.items():
            print(f"{keys}: {values}")

    else:
        print(f"Something went wrong.")
        print(f"Error code: {response['code']}")
        print(f"{response['message']}")
        os._exit(1)


def user_info():
    user_id = input("Enter the userId: ")
    token = getpass("Enter the user's token: ")

    user_req("get", {"userId": user_id, "token": token})


def register():
    username = input("Enter your username: ")
    email = input("Enter your email: ")

    pswrd = getpass("Enter your password: ")

    #Calculating the timeshift from UTC
    timeshift = datetime.now().astimezone().tzinfo.utcoffset(datetime.now()).seconds/3600

    print(timeshift)

    if getpass("Re-enter your password: ") != pswrd:
        print("Non-matching passwords!")
        os._exit(1)

    user_req("post", data = {"userName": username, "email": email, "password": pswrd, "timeShift, timeshift"})


def edit_profile(user_id):
    change_keys = input("Please enter settings you want to change: ").split(" ")
    new_settings = {"properties": dict()}

    for keys in change_keys:
        if keys == "password":
            print("Can't chane password via 'user' endpoint. Try: 'password'.")
            continue

        else:
            new_settings["properties"][keys] = input(f"Enter the new value for {keys}: ")

    new_settings["token"] = getpass("Enter your token: ")
    new_settings["properties"] = json.dumps(new_settings["properties"])

    user_req("patch", {"userId": user_id}, new_settings)


def delete_profile(user_id):
    confirm = input("Are you sure you want to delete your profile [Enter y for confirmation]: ").lower()

    if confirm == "y":
        pswrd = getpass("Please enter your password: ")

        user_req("delete", {"password": pswrd, "userId": user_id})

    print("Confirmaiton failed, stopping.")
    os._exit(1)


