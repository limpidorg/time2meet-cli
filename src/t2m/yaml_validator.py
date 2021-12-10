import yaml
import os
from getpass import getpass


#Creates a new yaml file if it doesn't exist.
#
def yaml_init():
    dirr = os.path.dirname(os.path.realpath(__file__)) + "/usrconf"
    if not os.path.isdir(dirr):
        os.makedirs(dirr)

    if not os.path.isfile(f"{dirr}/app.yaml"):
        yf = list(yaml_default())
        del yf[1]

        a_yf = [{"user_settings": {}}, {"app_settings": {}}]
        for keys in list(yf[0].keys()):
            a_yf[0]["user_settings"][keys] = None

        yf[1]["init"] = False

        for keys in list(yf[1].keys()):
            a_yf[1]["app_settings"][keys] = yf[1][keys]


        with open(f"{dirr}/app.yaml", "w+") as f:
            yaml.dump_all(a_yf, f, default_flow_style = False)

    return yaml_validate()


#Simple yaml manager to read and update app.yaml
#
def yaml_validate(skip_init = False):
    global def_dirr
    global yaml_dirr
    yaml_dirr = os.path.dirname(os.path.realpath(__file__)) + "/usrconf/app.yaml"
    def_dirr = os.path.dirname(os.path.realpath(__file__)) + "/defconf/def.yaml"

    #Parsing and checking the validation of the app.yaml using def.yaml for reference
    user, _, app = yaml_default()

    with open(yaml_dirr, "r") as f:
        yf = list(yaml.load_all(f, Loader=yaml.FullLoader))

        if len(yf) > 2:
            print("Extra file detected in app.yaml")
            os._exit(1)

        elif len(yf) < 2:
            print("Missing file in app.yaml")
            os._exit(1)

        if set(yf[0]["user_settings"].keys()) != set(user.keys()):
            print(f"YAML file broken. Missing settings in user_settings.")
            print(f"Expected: {set(user.keys())}, got {set(yf[0]['user_settings'].keys())}")
            os._exit(1)

        if yf[1]["app_settings"].keys() != set(app.keys()):
            print(f"YAML file broken. Missing settings in app_settings.")
            print(f"Expected: {set(app.keys())}, got {set(yf[1]['app_settings'].keys())}")
            os._exit(1)

        if skip_init:
            return yf

        #If this is the first time running, then we initiliaze the settings.
        if not yf[1]["app_settings"]["init"]:
            print("Initiliazing user.")
            existing_acc = input("Do you have an existing account? [y/n]: ")
            if existing_acc.lower() == "n":
                return "register"
            else:
                return "set_user"

        return yf


#Gets user settings
#
def yaml_user():
    yf = yaml_validate(True)

    return yf[0]["user_settings"]


#For formatting the data sent
#
def yaml_default():
    global def_dirr
    def_dirr = os.path.dirname(os.path.realpath(__file__)) + "/defconf/def.yaml"

    with open(def_dirr, "r") as f:
        def_yf = list(yaml.load_all(f, Loader=yaml.FullLoader))

    user = def_yf[0]["user_settings"]
    r = def_yf[1]["r_settings"]
    app = def_yf[2]["app_settings"]
    return user, r, app


#Updating user config
#
def yaml_update(update_key, update_value, reset = False):
    yf = yaml_validate(True)
    user, _, _ = yaml_default()
    #Creating a copy and modifiying said copy to then dump into app.yaml to update it.
    for files in yf:
        if reset:
            break
        if list(files.keys())[0] == "user_settings":

            if update_key == "password":
                continue

            if type(user[update_key]) != type(update_value):
                try:
                    update_value = eval(type(user[update_key]).__name__)(update_value)
                except:
                    print(f"""Invalid value entered for {update_key}. Expected {type(user[update_key]).__name__}, got {update_value}.""")

                    os._exit(1)

    yf[0]["user_settings"][update_key] = update_value

    if reset:
        yf[1]["app_settings"]["init"] = False

    else:
        yf[1]["app_settings"]["init"] = True

    with open(yaml_dirr, "w") as f:
        yaml.dump_all(yf, f, default_flow_style = False)
        print("Updated user settings.")

    #Finally, validating the updated file
    yaml_validate(True)


#Gets the base url
#
def base_url():
    with open(def_dirr, "r") as f:
        def_yf = list(yaml.load_all(f, Loader=yaml.FullLoader))
        
    return def_yf[2]["app_settings"]["base_url"]


#Reset the YAML file
#
def yaml_reset():
    for keys in yaml_user():
        yaml_update(keys, None, True)



