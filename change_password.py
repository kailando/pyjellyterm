from encrypt import JSONFernet
from inp import passw
from os import rename

op=passw("Old password: ")
fernet=JSONFernet(op, "servers.txt")
np=passw("New password: ")
fernet2=JSONFernet(np, "servers.txt.tmp")
fernet2.encrypt(fernet.decrypt())
del fernet
rename("servers.txt.tmp", "servers.txt")