import uuid


class Photo:
    uuid = ""
    photo = ""
    comment = ""
    date = None
    userUuid = ''
    latitude = 0
    longitude = 0

    def __init__(self, **kwargs):
        self.uuid = str(uuid.uuid4())
        self.photo = kwargs['photo']
        self.comment = kwargs['comment']
        self.date = kwargs['date']
        self.userUuid = kwargs['userUuid']
        self.latitude = kwargs['latitude']
        self.longitude = kwargs['longitude']
