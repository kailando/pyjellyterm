from base64 import urlsafe_b64encode as ub64
from hashlib import sha256
from json import dumps, loads
from os.path import exists

from cryptography.fernet import Fernet


class JSONFernet:
    def __init__(self, key, fp):
        self.fernet = None
        self.fp = None
        self.init(
            ub64(
                sha256(
                    key.encode("utf-8")
                ).digest()
            ), fp
        )
    
    def init(self, key, fp):
        self.fernet = Fernet(key)
        self.fp = fp

        if not exists(fp):
            self.encrypt({})
    
    def decrypt(self):
        res=None
        with open(self.fp, "rb") as f:
            res=loads(
                self.fernet.decrypt(
                    f.read()
                ).decode("utf-8")
            )
        return res
    
    def encrypt(self, json):
        with open(self.fp, "wb") as f:
            f.write(
                self.fernet.encrypt(
                    dumps(json).encode("utf-8")
                )
            )

    def __getitem__(self, key):
        return self.decrypt()[key]

    def __setitem__(self, key, value):
        data = self.decrypt()
        data[key] = value
        self.encrypt(data)
