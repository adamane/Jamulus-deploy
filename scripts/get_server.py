import time
from getpass import getpass

from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.locations.domain import Location
from hcloud.ssh_keys.client import SSHKeysClient
from hcloud.servers.client import  BoundServer
from hcloud.servers.domain import Server, PublicNetwork, IPv4Address
import random
import json
import paramiko
import sys


class Colors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


if input("This will cost money, if you really want to do that, type YES: ") != "YES":
    sys.exit(0)

with open("./deploy_config.json",mode="r",encoding="utf-8") as a:
    config = a.read()
config = json.loads(config)
serverName = config["name"] + str(random.randint(1000,9999))
client = Client(token=config["api_key"])  # Please paste your API token here between the quotes
if config["usePubKey"]:
    key = SSHKeysClient(client).get_by_name(config["pubKeyName"])

else:
    key = None
response = client.servers.create(name=serverName,
                                 server_type=ServerType(config["type"]),
                                 image=Image(name=config["image"]),
                                 location=Location(name=config["location"]),
                                 ssh_keys=key
                                 )
server = response.server
root_pw = response.root_password
server_id = server.id
print(Colors.OK + f"The Server was Requested" + Colors.RESET)
while server.status != "running":
    time.sleep(5)
    server = client.servers.get_by_id(server_id)

ip = server.model.public_net.ipv4.ip
print(f"The Server's IP address: {ip}")
print("Connencting and installing Jamulus")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# In case the server's key is unknown,
# we will be adding it automatically to the list of known hosts
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
# Loads the user's local known host file.
if config["usePubKey"]:
    PubKeyPasswd = getpass("Please Enter the Password of the SSH Key: ")
    privkey = paramiko.RSAKey.from_private_key_file(config["pubKeyPlace"])
    ssh.connect(ip, username="root", pkey=privkey)
else:
    ssh.connect(ip,username="root",password=root_pw)

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('curl -fsSL https://raw.githubusercontent.com/adamane/Jamulus-deploy/main/run_jamulus_on_docker.sh | bash')

time.sleep(120)
print("We should be done here")
ssh.close()
sys.exit(0)
