import json
import os


class Colors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


def addendum(val):
    global CONF_EXISTS, config
    try:
        if CONF_EXISTS:
            returner = f"(Old Value: {config[val]}): "
        else:
            returner = f"(Example: {config[val]}): "
    except Exception:
        returner = f": "
    return returner


def main():
    global CONF_EXISTS, config
    print("=" * 20)
    print("Autodeploy Jamulus")
    print("Create Config")
    print("=" * 20)

    if os.path.isfile("./deploy_config.json"):
        CONF_EXISTS = True
        with open("./deploy_config.json", mode="r") as a:
            config = json.loads(a.read())
        print(Colors.OK + "Found an existing Config File" + Colors.RESET)
    else:
        CONF_EXISTS = False
        with open("./sample_deploy_config.json", mode="r") as a:
            config = json.loads(a.read())
        print(Colors.WARNING + "Found no existing Config File" + Colors.RESET)
    required_params = ["name", "location", "usePubKey", "type", "image"]
    new_config = {}
    print(Colors.FAIL + "REQUIRED" + Colors.RESET)
    print("For the old or the example value, leave the field empty")

    new_config["name"] = str(input("Please enter the name " + addendum("name")))
    new_config["api_key"] = str(input("Please enter your HETZNER API key: "))
    new_config["location"] = str(input("Please enter the prefered locationcode " + addendum("location")))
    while True:
        usePubKey = input("Do you want to use Public Key authentification? (YES OR NO)" + addendum("usePubKey"))
        if usePubKey == "YES":
            new_config["usePubKey"] = True
            new_config["pubKeyName"] = str(
                input("Please enter the Name of the PubKey in HEZTNER" + addendum("pubKeyName")))
            break
        elif usePubKey == "NO":
            new_config["usePubKey"] = False
            break
        else:
            print("That was not a valid Choice!")
    new_config["type"] = str(input("Please enter the server Type " + addendum("type")))
    new_config["image"] = str(input("Please enter a image name " + addendum("image")))

    for i in required_params:
        if new_config[i] == "":
            new_config[i] = config[i]

    if new_config["usePubKey"]:
        if new_config["pubKeyName"] == "":
            new_config["pubKeyName"] = config["pubKeyName"]

    while True:
        if new_config["api_key"] == "" or new_config["api_key"] == "THIS_IS_SAMPLETEXT":
            print(Colors.FAIL + "The API key needs to be set" + Colors.RESET)
            new_config["api_key"] = str(input("Please enter your HETZNER API key: "))
        else:
            break

    new_config_json = json.dumps(new_config, ensure_ascii=False, indent=3)
    with open("./deploy_config.json", mode="w", encoding="UTF-8") as a:
        a.write(new_config_json)
    print(Colors.OK + "Created a Configfile" + Colors.RESET)


if __name__ == "__main__":
    main()
