import os
from request_handler import request
from datetime import datetime
import getpass


def __dir__():
    return ["create_planner", "edit_planner", "delete_planner", "get_planner"]

#Basic planner functions using Time2Meet API
def planner_req(protocol, param = None, data = None):
    response = request(protocol, "planner", param = param, data = data)

    if not response["code"]:
        for keys, values in response.items():
            print(f"{keys}: {values}")
    else:
        print(f"Something went wrong.")
        print(f"Error code: {response['code']}")
        print(f"{response['message']}")
        os._exit(1)


def create_planner(user_id, timeshift):
    token = getpass("Enter your token: ")
    meeting_name = input("Enter a name for your meeting: ")
    day, month, year = map(int, input("Please enter the date of the meeting in DD-MM-YYYY format: ").split("-"))
    start_hours, start_minutes = map(int, input("Enter the start time in HH/MM: ").split("/"))
    end_hours, end_minutes = map(int, input("Enter the end time in HH/MM: ").split("/"))

    if end_hours < start_hours:
        diff = timedelta(days = 1)

    start = datetime(year, month, day, start_hours, start_minutes).timestamp()-timeshift*3600
    end = (datetime(year, month, day, end_hours, end_minutes) + diff).timestamp()-timeshift*3600
    
    planner_req("post", {"plannerName": meeting_name, "userId": user_id, "token": token, "plannerName": meeting_name}, {"notBefore" : end, "notAfter": start})

def edit_planner(planner_id):
    token = getpass("Enter your token: ")
    settings = input("Please enter the settings you want to change:").split()
    properties = dict()

    for k in settings:
        properties[k] = input(f"{k}: ")

    planner_req("patch", {"token": token, "plannerId": planner_id, "properties": properties})


def delete_planner(planner_id):
    try:
        if input("Are you sure that you want to delete the planner? (Type 'y' to delete): ").lower() == "y":
            planner_req("delete", {"plannerId": planner_id})
        else:
            print("Confirmation failed, stopping.")
    except:
        print("Confirmation failed, stopping.")

def get_planner(planner_id):
    planner_req("get", {"plannerId": planner_id})
