import os
from getpass import getpass
from request_handler import request
from yaml_validator import yaml_user


def __dir__():
    return ["change_password"]


def password_req(protocol, param = None, data = None):
    response = request(protocol, "password", param = param, data = data)


#Simple password changer
def change_password():
    pswrd = getpass("Enter your password: ")

    if not pswrd == getpass("Re-enter your password: "):
        print("Non-matching passwords entered, stopping.")
        os._exit(1)

    new_pswrd = getpass("Enter your new password: ")
    
    if not new_pswrd == getpass("Re-enter your new password: "):
        print("Non-matching passwords entered, stopping.")
        os._exit(1)

    password_req("patch", {"password":  pswrd, "userId": yaml_user()["userId"]}, {"password": new_pswrd})


