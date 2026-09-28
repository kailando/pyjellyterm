"""Change the password to your client."""

from os import rename
from encrypt import JSONFernet
from inp import passw

op=passw("Old password: ")
fernet=JSONFernet(op, "servers.txt")
np=passw("New password: ")
fernet2=JSONFernet(np, "servers.txt.tmp")
fernet2.encrypt(fernet.decrypt())
del fernet
rename("servers.txt.tmp", "servers.txt")
