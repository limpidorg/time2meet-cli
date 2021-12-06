import yaml
import os
import get
#Simple yaml manager to read and update app.yaml
#

def yaml_validate():
    yaml_dirr = os.getcwd() + "/usrconf/app.yaml"
    def_dirr = os.getcwd() + "/defconf/def.yaml"


    #Parsing and checking the validation of the def_

    with open(def_dirr, "r") as f:
        def_yf = list(yaml.load_all(f, Loader=yaml.FullLoader))

    with open(yaml_dirr, "r") as f:

        file_broken = False
        yf = list(yaml.load_all(f, Loader=yaml.FullLoader))
        if len(yf) > 3:
            print("Extra file detected in app.yaml")
            os._exit(1)
        elif len(yf) < 3:
            print("Missing file in app.yaml")
            os._exit(1)
        for i in range(3):
            try:
                if yf[i]["user_settings"].keys() != set(def_yf[i]["user_settings"].keys()):
                    print(f"YAML file broken. Missing settings in user_settings.")
                    print(f"Expected: {list(def_yf[i]['user_settings'].keys())}, got {list(yf[i]['user_settings'].keys())}")
                    os._exit(1)

            except:
                try:
                    if yf[i]["r_settings"].keys() != def_yf[i]["r_settings"].keys():
                        print(f"YAML file broken. Missing settings in r_settings.")
                        print(f"Expected: {list(def_yf[i]['r_settings'].keys())}, got {list(yf[i]['r_settings'].keys())}")
                        os._exit(1)

                except:
                    if yf[i]["app_settings"].keys() != def_yf[i]["app_settings"].keys():
                        print(f"YAML file broken. Missing settings in app_settings.")
                        print(f"Expected: {list(def_yf[i]['app_settings'].keys())}, got {list(yf[i]['app_settings'].keys())}")
                        os._exit(1)

        if not yf[2]["app_settings"]["init"]:
            print("Initiliazing user.")
            existing_acc = input("Do you have an existing account? [y/n]:")
            # TODO: Implement creating of new user
            if existing_acc.lower() == "n":
                pass
            else:
                username = input("Please enter your username: ")
                email = input("Please enter your email: ")




def yaml_manage(update = False, update_key = None, update_value = None):

    #Use global directory and file.
    global yaml_dirr, yaml_files

    #Finding app.yaml.
    
    if not update:
        return yf


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


