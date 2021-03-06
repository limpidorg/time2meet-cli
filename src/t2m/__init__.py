import os

from .planner import *
from .user import *
from .tokens import *
from .yaml_validator import *
from .request_handler import set_dry

set_dry(False)
validation = yaml_init()

#Logging/Register the user
#
if validation == "set_user" or validation == "register":

    if validation == "set_user":
        dry_resp = dict()
        usr, tok = user_info(True)

        for keys in list(yaml_user().keys()):
            if keys == "require-email-verification":
                if usr["user"]["status"] == "require-email-verification":
                    yaml_update("require-email-verification", True)
                    continue
                elif usr["user"]["status"] == "active":
                    yaml_update("require-email-verification", False)
                    continue

            if keys not in list(usr["user"].keys()) and keys != "require-email-verification":
                continue

            print(keys)
            yaml_update(keys, usr["user"][keys]) 

        get_list_planners(tok)

    if validation == "register":
        register()

#If the user didn't verify their email, verify it
#
if yaml_user()["require-email-verification"]:
    verify_email()

#Removing old planners
#
print("Init complete!")

