import uuid
from datetime import datetime


class User:
    email = ""
    password = ""
    nickname = ""
    avatar = ""
    registrationDate = None

    def __init__(self, **kwargs):
        self.uuid = str(uuid.uuid4())
        self.registrationDate = datetime.utcnow().strftime(r"%y/%m/%d %H:%M:%S")
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.nickname = kwargs['nickname']
        self.avatar = kwargs['avatar']
