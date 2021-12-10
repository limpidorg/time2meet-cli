import os
from getpass import getpass
from .request_handler import request
from .yaml_validator import yaml_user, yaml_update, yaml_reset
from .tokens import new_token
from datetime import  datetime
import json


def __dir__():
    return ["user_info", "register", "edit_profile", "delete_profile"]


def user_req(protocol, param = None, data = None):
    return request(protocol, "user", param = param, data = data)
 

#Print out current user_info
#
def user_info(user_id = None):
    if user_id is None:
        user_id = input("Enter the userId: ")

    tok = getpass("Enter the user's token: ")

    user_req("get", {"userId": user_id, "token": tok})


#Register a new account and set the account for this computer
#
def register():
    username = input("Enter your username: ")
    email = input("Enter your email: ")

    pswrd = getpass("Enter your password: ")

    #Calculating the timeshift from UTC
    timeshift = datetime.now().timestamp() - datetime.utcnow().timestamp()

    if getpass("Re-enter your password: ") != pswrd:
        print("Non-matching passwords!")
        os._exit(1)
    data = {"userName": username, "email": email, "password": pswrd, "timeShift": timeshift} 

    if user_req("post", data = data):
        for keys, values in data.items():
            if keys == "password":
                continue

            yaml_update(keys, values, False)

        user_id = input("Enter your userId: ")
        yaml_update("userId", user_id, False)
        new_token(email, pswrd)

        request("post", "email-verification", param = {"userId": user_id, "otp": input("Enter your verificiation code sent to your email: "), "token": getpass("Please enter your token: ")})

    else:
        os._exit(1)


#Change profile settings
#
def edit_profile():
    change_keys = input("Please enter settings you want to change: ").split(" ")
    new_settings = {"properties": dict()}

    for keys in change_keys:
        if keys == "password":
            print("Can't chane password via 'user' endpoint. Try: 'password'.")
            continue

        else:
            if keys == "timeShift":
                change = datetime.timedelta(hours = float(input("Enter the difference from UTC in hours: "))).seconds
            else:
                change = input(f"Enter the new value for {keys}: ")

            new_settings["properties"][keys] = change

    tok = getpass("Enter your token: ")
    new_settings["properties"] = json.dumps(new_settings["properties"])

    if user_req("patch", {"userId": yaml_user()["userId"], "token": tok}, new_settings):
        for keys in list(new_settings["properties"].keys()):
            yaml_update(keys, new_settings["properties"][keys])


#Delete profile
#
def delete_profile():
    confirm = input("Are you sure you want to delete your profile [Enter 'confirm' for confirmation]: ")

    if confirm == "confirm":
        pswrd = getpass("Please enter your password: ")
        if user_req("delete", {"password": pswrd, "userId": yaml_user()["userId"]}):
            yaml_reset()
            os._exit(1)

    else:
        print("Confirmaiton failed, stopping.")
        os._exit(1)


