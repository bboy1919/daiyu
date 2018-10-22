import hashlib
from settings import Config


def md5(arg):
    ihash = hashlib.md5(Config.SALT)
    ihash.update(bytes(arg, encoding='utf-8'))
    return ihash.hexdigest()
