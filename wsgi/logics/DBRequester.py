import base64
from datetime import datetime
import os

from io import BytesIO
import jsonpickle
import pymongo
import json
from PIL import Image

from wsgi.models.Photo import Photo
from wsgi.models.User import User


class UserExistsError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class UserMissingError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class DBRequester:
    db = None
    MONGODB_DB_URL = ""
    MONGODB_DB_NAME = ""

    def __init__(self):
        self.MONGODB_DB_URL = os.environ.get('MONGODB_URL') if os.environ.get(
            'MONGODB_URL') else 'mongodb://localhost:27017/'
        self.MONGODB_DB_NAME = os.environ.get('OPENSHIFT_APP_NAME') if os.environ.get(
            'OPENSHIFT_APP_NAME') else 'photoservice'
        client = pymongo.MongoClient(self.MONGODB_DB_URL)
        self.db = client[self.MONGODB_DB_NAME]

    def GetUserByUuid(self, user_uuid: str):
        user = self.db.get_collection('users').find_one({'uuid': user_uuid}, {'_id': None})
        json_string = json.dumps(user)
        return jsonpickle.decode(json_string)

    def GetUserByCredentials(self, email: str, password: str):
        user = self.db.get_collection('users').find_one({'email': email, 'password': password}, {'_id': None})
        return jsonpickle.decode(json.dumps(user)) if user else None

    def AddUser(self, email: str, password: str, nickname: str, avatar_dict: dict):
        user = self.GetUserByCredentials(email, password)
        if user:
            raise UserExistsError("User already exists")

        if avatar_dict is not None:
            base64image = str(base64.b64encode(avatar_dict['body']))
        else:
            jpeg_image_buffer = BytesIO()
            Image.new("RGB", (320, 320), (197, 207, 224)).save(jpeg_image_buffer, format="PNG")
            base64image = str(base64.b64encode(jpeg_image_buffer.getvalue()))

        user = User(
                email=email,
                password=password,
                nickname=nickname,
                avatar=base64image[2:-1]
            )
        user_json = jsonpickle.encode(user)
        encoded_to_dict = json.loads(user_json)
        self.db.get_collection('users').insert(encoded_to_dict)
        return user

    def UpdateUser(self, user_uuid: str, nickname: str, avatar_dict: dict):
        user = self.GetUserByUuid(user_uuid)
        if not user:
            raise UserMissingError("User not exists")

        if nickname is not None:
            user.nickname = nickname

        if avatar_dict is not None:
            path = user.avatar_path
            file = open(path, 'wb')
            file.write(avatar_dict['body'])
            file.close()
            user.avatar = str(base64.b64encode(avatar_dict['body']))[2:-1]

        self.db.get_collection('users').update_one(
            self.db.get_collection('users').find_one({'uuid': user.uuid}),
            {"$set": json.loads(jsonpickle.encode(user))},
            upsert=False)
        return self.GetUserByUuid(user.uuid)

    def AddPhoto(self, user_uuid: str, comment: str, latitude: str, longitude: str, photo_dict: dict):
        base64image = str(base64.b64encode(photo_dict['body']))

        photo_json = jsonpickle.encode(
            Photo(photo=base64image[2:-1],
                  userUuid=user_uuid,
                  date=str(datetime.utcnow().strftime(r"%y/%m/%d %H:%M:%S")),
                  comment=comment,
                  latitude=latitude,
                  longitude=longitude)
            )

        encoded_to_dict = json.loads(photo_json)
        return self.db.get_collection('photos').insert(encoded_to_dict)

    def GetPhotoByUuid(self, photo_uuid: str):
        photo = self.db.get_collection('photos').find_one({'uuid': photo_uuid}, {'_id': None})
        return jsonpickle.decode(json.dumps(photo))

    def GetPhotoByUuid(self, photo_uuid: str):
        photo = self.db.get_collection('photos').find_one({'uuid': photo_uuid}, {'_id': None})
        return jsonpickle.decode(json.dumps(photo)) if photo else None

    def GetRandomPhoto(self):
        photo = self.db.get_collection('photos').aggregate(
            [
                {'$sample': {'size': 1}},
                {'$addFields': {'_id': None}}
            ]
        )
        return jsonpickle.decode(json.dumps(photo.next())) if photo else None

    def GetRandomPhotos(self):
        photos = self.db.get_collection('photos').aggregate(
            [
                {'$sample': {'size': 10}},
                {'$addFields': {'_id': None, 'photo': None}}
            ]
        )
        return jsonpickle.decode(json.dumps(list(photos))) if photos else None
