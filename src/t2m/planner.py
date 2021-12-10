import os
from .request_handler import request
from .yaml_validator import yaml_user, yaml_update
from datetime import datetime, timedelta
from getpass import getpass
import json


def list_methods():
    return ["create_planner", "edit_planner", "delete_planner", "get_planner", "get_list_planners"]


#Basic planner functions using Time2Meet API
def planner_req(protocol, param = None, data = None):
    return request(protocol, "planner", param = param, data = data)


def calculate_time():
    day, month, year = map(int, input("Please enter the date of the meeting in DD-MM-YYYY format: ").split("-"))
    start_hours, start_minutes = map(int, input("Enter the start time in HH/MM: ").split("/"))
    end_hours, end_minutes = map(int, input("Enter the end time in HH/MM: ").split("/"))

    timeshift = yaml_user()["timeShift"]
    diff = timedelta(days = 0)
    if end_hours < start_hours:
        diff = timedelta(days = 1)

    start = datetime(year, month, day, start_hours, start_minutes).timestamp()-timeshift*3600
    end = (datetime(year, month, day, end_hours, end_minutes) + diff).timestamp()-timeshift*3600

    return start, end


#Create a planner
#
def create_planner():
    tok = getpass("Enter your token: ")
    meeting_name = input("Enter a name for your meeting: ")

    start, end = calculate_time()

    resp = planner_req("post", {"plannerName": meeting_name, "userId": user_id, "token": tok, "plannerName": meeting_name}, {"notBefore" : end, "notAfter": start})

    if resp:
        try:
            curr_planners = list(yaml_user()["planners"])
        except:
            curr_planners = list()
        yaml_update("planners", curr_planners.append(resp["plannerId"]))


#Edit an existing planner
#
def edit_planner():
    tok = getpass("Enter your token: ")
    get_list_planners(tok)
    planner_id = input("Enter plannerId: ")
    meeting_name = input("Enter a new meeting name for your meeting: ")

    start, end = calculate_time()

    properties = {"notBefore": start, "notAfter": end, "plannerName": meeting_name}
    planner_req("patch", {"userId": yaml_user()["userId"],"token": tok, "plannerId": planner_id, "properties": json.dumps(properties)})


#Delete an existing planner
#
def delete_planner(planner_id, remove_old = False):
    if remove_old:
        if datetime.fromtimestamp(get_planner(planner_id)["notAfter"] + yaml_user()["timeShift"]) < datetime.now().timestamp():
            yaml_update("planners", yaml_user()["planners"].remove("planner_id"))

    try:
        if input("Are you sure that you want to delete the planner? (Type 'confirm' to delete): ").lower() == "confirm":
            tok = getpass("Enter your token: ")
            planner_req("delete", {"plannerId": planner_id[0], "token": tok, "userId": yaml_user()["userId"]})
        else:
            print("Confirmation failed, stopping.")
    except:
        print("Confirmation failed, stopping.")


#Get planner details
#
def get_planner(planner_id, tok = None):
    if tok is None:
        tok = getpass("Enter your token: ")

    return planner_req("get", {"plannerId": planner_id, "token": tok, "userId": yaml_user()["userId"]})


#Get all active planners
#
def get_list_planners(tok = None):
    if tok is None:
        tok = getpass("Enter your token: ")

    planners = request("get", "planners", param = {"token": tok, "userId": yaml_user()["userId"]})

    curr_planners = list()

    for planner_id in planners["plannerIds"]: 
        curr_planners.append(planner_id)

        print(get_planner(planner_id, tok))

    yaml_update("planners", curr_planners)


