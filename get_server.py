from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.locations.domain import Location
from hcloud.ssh_keys.domain import SSHKey
import random
import json
import sys

if input("This will cost money, if you really want to do that, type YES: ") != "YES":
    sys.exit(0)

with open("./deploy_config.json",mode="r",encoding="utf-8") as a:
    config = a.read()
config = json.loads(config)
serverName = config["name"] + str(random.randint(1000,9999))
client = Client(token=config["api_key"])  # Please paste your API token here between the quotes
if config["usePubKey"]:
    key = SSHKey(name=config["pubKeyName"])
else:
    key = None
response = client.servers.create(name=serverName,
                                 server_type=ServerType(config["type"]),
                                 image=Image(name=config["image"]),
                                 location=Location(name=config["location"]),
                                 ssh_keys=key
                                 )
server = response.server
print(server)
print("Root Password: " + response.root_password)
