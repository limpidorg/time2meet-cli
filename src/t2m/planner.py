import os
from .request_handler import request
from .yaml_validator import yaml_user, yaml_update
from datetime import datetime
from getpass import getpass


def __dir__():
    return ["create_planner", "edit_planner", "delete_planner", "get_planner", "get_list_planner"]


#Basic planner functions using Time2Meet API
def planner_req(protocol, param = None, data = None):
    return request(protocol, "planner", param = param, data = data)


#Create a planner
#
def create_planner():
    tok = getpass("Enter your token: ")
    meeting_name = input("Enter a name for your meeting: ")
    day, month, year = map(int, input("Please enter the date of the meeting in DD-MM-YYYY format: ").split("-"))
    start_hours, start_minutes = map(int, input("Enter the start time in HH/MM: ").split("/"))
    end_hours, end_minutes = map(int, input("Enter the end time in HH/MM: ").split("/"))

    timeshift = yaml_user()["timeShift"]
    user_id = yaml_user()["userId"]

    if end_hours < start_hours:
        diff = timedelta(days = 1)

    start = datetime(year, month, day, start_hours, start_minutes).timestamp()-timeshift*3600
    end = (datetime(year, month, day, end_hours, end_minutes) + diff).timestamp()-timeshift*3600

    resp = planner_req("post", {"plannerName": meeting_name, "userId": user_id, "token": tok, "plannerName": meeting_name}, {"notBefore" : end, "notAfter": start})

    if resp:
        yaml_update("plannerId", yaml_user()["planner"].append(resp[plannerId]))


#Edit an existing planner
#
def edit_planner():
    get_list_planner()
    planner_id = input("Enter plannerId: ")
    tok = getpass("Enter your token: ")
    settings = input("Please enter the settings you want to change:").split()
    properties = dict()

    for k in settings:
        properties[k] = input(f"{k}: ")

    planner_req("patch", {"token": tok, "plannerId": planner_id, "properties": properties})


#Delete an existing planner
#
def delete_planner(planner_id, remove_old = False):
    if remove_old:
        if datetime.fromtimestamp(get_planner(planner_id)["notAfter"] + yaml_user()["timeShift"]) < datetime.now().timestamp():
            yaml_update("planners", yaml_user()["planners"].remove("planner_id"))

    try:
        if input("Are you sure that you want to delete the planner? (Type 'confirm' to delete): ").lower() == "confirm":
            pswrd = getpass("Enter your password: ")
            planner_req("delete", {"plannerId": planner_id, "password": pswrd})
        else:
            print("Confirmation failed, stopping.")
    except:
        print("Confirmation failed, stopping.")


#Get planner details
#
def get_planner(planner_id):
    return planner_req("get", {"plannerId": planner_id})


#Get all active planners.
#
def get_list_planner():
    for planners in yaml_user()["planners"]:
        get_planner("planners")
