from socket import gethostname
from sys import exit

from jellyfin_apiclient_python import JellyfinClient
from jellyfin_apiclient_python.connection_manager import CONNECTION_STATE

from inp import *

# Setup
client = JellyfinClient()
client.config.app(
    "PyJellyTerm",
    "0.1.0",
    gethostname(),
    "pyjellyterm"
)
client.config.data["auth.ssl"] = False

# Connect to server
server = input("Server: ")
res = client.auth.connect_to_address(server)["State"]
if res == CONNECTION_STATE.Unavailable:
    exit(1)

# Print users
print("Users:")
u=client.auth.get_public_users()
up={item['Name']: item['HasPassword'] for item in u}
users=list(up.keys())

username = get_from_list(users, "Users:", f"Username: (1-{len(users)}) ")

# Get password if needed
if up[username]:
    password=passw("Password: ")

# Log in
print("Logging in...")
client.auth.login(server, username, password)
print("Done logging in!")

# Lil thing to test
j=client.jellyfin
results=j.search_media_items(term=input("Query: "), media="Movies")

for item in results["Items"]:
    if item["IsFolder"]:
        print(f"FOLDER: {item['Name']} ({item['Type']})")
        continue
    print(f"{item['Name']} ({item.get('ProductionYear', '?')}) {item.get('OfficialRating', '?')}")
