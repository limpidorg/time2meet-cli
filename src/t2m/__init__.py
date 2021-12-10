import os

from .planner import *
from .user import *
from .tokens import *
from .yaml_validator import *
from .request_handler import set_dry

validation = yaml_init()

#Logging/Register the user
#
if validation == "set_user" or validation == "register":
    d = input("Enable dry run for register/login? [y/n]: ").lower()

    if d == "y":
        set_dry(True)

    else:
        set_dry(False)

    if validation == "set_user":
        dry_resp = dict()
        usr = user_info()

        for keys in list(yaml_user().keys()):
            if keys not in ["userId","email","timeShift","userName","planner", "status"]:
                continue
            if keys == "require-email-verificaiton":
                if usr["user"]["status"] == "require-email-verifcation":
                    yaml_update("require-email-verification", True)
                    continue
            yaml_update(keys, usr["user"][keys]) 

        os._exit(1)

    if validation == "register":
        data = register()

#If the user didn't verify their email, verify it
#
if yaml_user()["require-email-verification"]:
    verify_email()

#Removing old planners
#
if yaml_user()["planners"] is not None:
    print("Deleteing old planners")
    for p in yaml_user()["planners"]:
        delete_planner(p, True)

print("Init complete!")


