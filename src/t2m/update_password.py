import os
from getpass import getpass
from .request_handler import request
from .yaml_validator import yaml_user


def list_methods():
    return ["change_password", "reset_password"]


def password_req(protocol, param = None, data = None):
    return request(protocol, "password", param = param, data = data)


#Simple password changer
#
def change_password():
    pswrd = getpass("Enter your password: ")

    if not pswrd == getpass("Re-enter your password: "):
        print("Non-matching passwords entered, stopping.")
        os._exit(1)

    while True:
        new_pswrd = getpass("Enter your new password: ")

        if not new_pswrd == getpass("Re-enter your new password: "):
            print("Non-matching passwords entered, stopping.")
            os._exit(1)

    password_req("patch", {"password":  pswrd, "userId": yaml_user()["userId"]}, {"password": new_pswrd})

#Resetting the password if the user forgets
#
def reset_password():
    if password_req("get", {"userId": yaml_user()["userId"]}):
        while True:
            new_pswrd = getpass("Enter your new password: ")

            if new_pswrd != getpass("Re-enter your new password: "):
                print("Passwords don't match!")
                continue

            break
        password_req("post", {"userId": yaml_user()["userId"], "password": new_pswrd, "otp": input(f"Enter the verification code sent to {yaml_user()['email']}")})
