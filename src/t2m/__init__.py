from .planner_handler import planner
from .account_manager import login, register, edit_profile, delete_profile, user
from .yaml_validator import yaml_validate, yaml_update


validation = yaml_validate()

if validation == "login" or validation == "register":
    cred = globals()[validation]

    if validation == "register":
        validation = "user"

    response = user("post", yaml_validate(True)["app_settings"]["base_url"], validation, data = cred)
