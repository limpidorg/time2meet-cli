import yaml
import os
import getpass
#Simple yaml manager to read and update app.yaml
#
def yaml_validate(skip_init = False):
    yaml_dirr = os.getcwd() + "/usrconf/app.yaml"
    def_dirr = os.getcwd() + "/defconf/def.yaml"

    #Parsing and checking the validation of the app.yaml using def.yaml for reference
    print("Validationg YAML file.")
    with open(def_dirr, "r") as f:
        def_yf = list(yaml.load_all(f, Loader=yaml.FullLoader))

    with open(yaml_dirr, "r") as f:

        yf = list(yaml.load_all(f, Loader=yaml.FullLoader))
        if len(yf) > 2:
            print("Extra file detected in app.yaml")
            os._exit(1)
        elif len(yf) < 2:
            print("Missing file in app.yaml")
            os._exit(1)
        for i in range(2):
            try:
                if yf[i]["user_settings"].keys() != set(def_yf[i]["user_settings"].keys()):
                    print(f"YAML file broken. Missing settings in user_settings.")
                    print(f"Expected: {list(def_yf[i]['user_settings'].keys())}, got {list(yf[i]['user_settings'].keys())}")
                    os._exit(1)

            except:
                if yf[i]["app_settings"].keys() != def_yf[i]["app_settings"].keys():
                    print(f"YAML file broken. Missing settings in app_settings.")
                    print(f"Expected: {list(def_yf[i]['app_settings'].keys())}, got {list(yf[i]['app_settings'].keys())}")
                    os._exit(1)

        print("YAML file valid.")

        if skip_init:
            return yf

        #If this is the first time running, then we initiliaze the settings.
        if not yf[2]["app_settings"]["init"]:
            print("Initiliazing user.")
            existing_acc = input("Do you have an existing account? [y/n]:")
            if existing_acc.lower() == "n":
                return "login"
            else:
                return "register"

        return yf

#Gets user settings
#
def yaml_user():
    yf = yaml_validate(True)

    return yf[0]["user_settings"]

#For formatting the data sent
#
def yaml_default():
    with open(def_dirr, "r") as f:
        def_yf = list(yaml.load_all(f, Loader=yaml.FullLoader))
    user = def_yf[0]
    r = def_yf[1]
    return user, r


#Updating user config
#
def yaml_update(update_key = None, update_value = None, init = False):
    yf = yaml_validate(init)
    #Creating a copy and modifiying said copy to then dump into app.yaml to update it.
    for files in yf:
        if list(files.keys())[0] == "user_settings":
            if  type(files["user_settings"][update_key]) != type(update_value):
                try:
                    update_value = eval(type(files["user_settings"][update_key]).__name__)(update_value)
                except:
                    print(f"""Invalid value entered for {files['user_settings'][update_key]}.
                            Expected {type(files['user_settings'][update_key]).__name__}, got {type(update_value).__name}.""")
                    quit()
            files["user_settings"][update_key] = update_value
            break

    with open(yaml_dirr, "w") as f:
        yaml.dump_all(yf, f, default_flow_style = False)
        print("Updated user settings.")

    #Finally, validating the updated file
    yaml_validate()


def base_url():
    with open(def_dirr, "r") as f:
        def_yf = list(yaml.load_all(f, Loader=yaml.FullLoader))
        
    return def_yf[2]["app_settings"]["base_url"]
