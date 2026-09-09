from base64 import urlsafe_b64encode as ub64
from collections import UserDict
from hashlib import sha256
from json import dumps, loads
from os.path import exists

from cryptography.fernet import Fernet


class EncryptedView(UserDict):
    """A proxy dictionary that forwards all structural changes back to the root JSONFernet object."""
    def __init__(self, root, path, initial_data):
        # Assign attributes first before filling data to prevent initialization crash
        self._root = root
        self._path = path
        self.data = initial_data  # Fill internal storage directly to skip triggering __setitem__ loops

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if isinstance(value, dict) and not isinstance(value, EncryptedView):
            # Wrap child dicts on the fly as they are accessed
            return EncryptedView(self._root, self._path + [key], value)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._sync_root()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._sync_root()

    def _sync_root(self):
        # Traverse down the root's fresh decrypted data to find where to inject our state
        data = self._root.decrypt()
        target = data
        for step in self._path[:-1]:
            target = target[step]
        
        # Update the root tree with our local modifications and write to disk
        if self._path:
            target[self._path[-1]] = dict(self.data)
            self._root.encrypt(data)
        else:
            self._root.encrypt(dict(self.data))


class JSONFernet:
    def __init__(self, key: str, fp: str):
        self.fernet = None
        self.fp = None
        self.init(
            ub64(
                sha256(
                    key.encode("utf-8")
                ).digest()
            ), fp
        )
    
    def init(self, key: bytes, fp: str):
        self.fernet = Fernet(key)
        self.fp = fp

        if not exists(fp):
            self.encrypt({})
    
    def decrypt(self) -> dict:
        with open(self.fp, "rb") as f:
            return loads(
                self.fernet.decrypt(
                    f.read()
                ).decode("utf-8")
            )
    
    def encrypt(self, json_data: dict):
        with open(self.fp, "wb") as f:
            f.write(
                self.fernet.encrypt(
                    dumps(json_data).encode("utf-8")
                )
            )

    def _get_root_view(self):
        return EncryptedView(self, [], self.decrypt())

    def __getitem__(self, key: str):
        return self._get_root_view()[key]

    def __setitem__(self, key: str, value):
        view = self._get_root_view()
        view[key] = value

    def __delitem__(self, key: str):
        view = self._get_root_view()
        del view[key]

    def __contains__(self, key: str) -> bool:
        return key in self.decrypt()

    def get(self, key: str, default=None):
        return self._get_root_view().get(key, default)

    def items(self):
        return self._get_root_view().items()

    def keys(self):
        return self._get_root_view().keys()

    def values(self):
        return self._get_root_view().values()
        
    def __iter__(self):
        return iter(self._get_root_view())
