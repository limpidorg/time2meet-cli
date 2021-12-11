import os
from getpass import getpass
from .request_handler import request
from .yaml_validator import yaml_user


def list_methods():
    return ["update_permission"]


def user_permissions_req(protocol, param = None, data = None):
    return request(protocol, "user-permissions", param = param, data = data)


#Create a new token
#
def update_permission():
    target = input("Enter the userId of the person you want to change the permissions of: [Leave blank if you want to change your own permissions] ")
    planner_id = input("Enter the plannerId: ")
    perms = input("Enter new permissions: [Leave blank if you want to remove the user]").split()
    tok = getpass("Enter your token: ")

    if target:
        user_permissions_req("patch", {"userId": yaml_user()["userId"], "token": tok, "permissions": perms, "plannerId": planner_id})
    else:
        user_permissions_req("patch", {"userId": yaml_user()["userId"], "token": tok, "permissions": perms, "plannerId": planner_id}, {"targetUserId": target})


