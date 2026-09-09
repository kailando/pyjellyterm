from socket import gethostname
from sys import exit

from jellyfin_apiclient_python import JellyfinClient
from jellyfin_apiclient_python.connection_manager import CONNECTION_STATE

from encrypt import JSONFernet
from inp import *

# Setup
servers = JSONFernet(passw("Password: "), "servers.txt")

client = JellyfinClient()
client.config.app(
    "PyJellyTerm",
    "0.1.0",
    gethostname(),
    "pyjellyterm"
)
client.config.data["auth.ssl"] = False

# Connect to server

def try_connect(server):
    res = client.auth.connect_to_address(server)["State"]
    if res == CONNECTION_STATE.Unavailable:
        exit(1)

name = get_from_list(list(servers.decrypt().keys()), "Saved servers (esc to enter custom):")
if name is None:
    server = input("Server: ")
    try_connect(server)
    if input("Save? (y/n) ").lower()=="y":
        name = input("Server name: ")
        servers[name]={"address": server, "users": {}}
else:
    server = servers[name]["address"]
    try_connect(server)


# Print users
used_custom = False
u=servers[name]["users"]
up={name: item['has_password'] for name, item in u.items()}
users=list(up.keys())
username=get_from_list(users, "Saved users (esc to go to full list):")

if username is None:
    used_custom = True
    client.auth.connect_to_address(server)
    u=client.auth.get_public_users()
    up={item['Name']: item['HasPassword'] for item in u}
    users=list(up.keys())
    username=get_from_list(users, "Users (esc to exit):")

    if username is None:
        exit(0)

# Get password if needed
if used_custom and up[username]:
    password=passw("Password: ")
elif up[username]:
    password=servers[name]["users"][username]["password"]

if used_custom and (input("Save? (y/n) ").lower()=="y"):
    servers[name]["users"][username] = (
        {
            "has_password": True,
            "password": password
        } if up[username] else {
            "has_password": False
        }
    )

# Log in
print("Logging in...")
client.auth.login(server, username, password)
print("Done logging in!")

# Trying to be secure (:
if "password" in globals():
    password=" "*(len(password)+3)
    password=0
    password=None
    del password

j=client.jellyfin

while True:
    try:
        results=j.search_media_items(term=input("Query: "), media="Movies")
    except (EOFError, KeyboardInterrupt):
        break

    if not results["Items"]:
        print("No results.")
        continue

    folders=[]
    for item in results["Items"]:
        if item["IsFolder"]:
            folders.append(item)
            continue
        print(f"{item['Name']} ({item.get('ProductionYear', '?')}) {item.get('OfficialRating', '?')}")
    print("\nFolders: ")
    for item in folders:
        print(f"{item['Name']} ({item['Type']})")