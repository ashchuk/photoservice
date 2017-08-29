import jsonpickle

from wsgi.handlers.BaseHandler import *
from wsgi.logics.DBRequester import DBRequester


class AddPhoto(BaseHandler):
    @cacheProtectorDecorator
    def post(self):
        if not self.get_current_user():
            raise tornado.HTTPError(404)

        user_uuid = self.get_current_user().decode(encoding='UTF-8')
        comment = tornado.escape.url_unescape(self.get_argument('comment'), encoding='utf-8', plus=True)
        latitude = tornado.escape.url_unescape(self.get_argument("latitude"), encoding='utf-8', plus=True)
        longitude = tornado.escape.url_unescape(self.get_argument("longitude"), encoding='utf-8', plus=True)
        image = self.request.files['filearg'][0]

        DBRequester().AddPhoto(user_uuid, comment, latitude, longitude, image)

        self.write("Successfully add photo!")


class GetPhotoByUuid(BaseHandler):
    @cacheProtectorDecorator
    def get(self):
        if not self.get_current_user():
            raise tornado.HTTPError(404)

        self.set_header('Content-Type', 'application/json')

        photo_uuid = tornado.escape.url_unescape(self.get_argument('photoUuid'), encoding='utf-8', plus=True)
        photo = DBRequester().GetPhotoByUuid(photo_uuid)

        self.write(jsonpickle.encode(photo, unpicklable=False))
        self.finish()


class GetRandomPhoto(BaseHandler):
    @cacheProtectorDecorator
    def get(self):
        if not self.get_current_user():
            raise tornado.HTTPError(404)

        self.set_header('Content-Type', 'application/json')

        photo = DBRequester().GetRandomPhoto()

        self.write(jsonpickle.encode(photo, unpicklable=False))
        self.finish()


class GetPhotos(BaseHandler):
    @cacheProtectorDecorator
    def get(self):
        if not self.get_current_user():
            raise tornado.HTTPError(404)

        self.set_header('Content-Type', 'application/json')

        photos = DBRequester().GetRandomPhotos()

        self.write(jsonpickle.encode(photos, unpicklable=False))
        self.finish()


class GetBase64ImageByPhotoUuid(BaseHandler):
    @cacheProtectorDecorator
    def get(self):
        if not self.get_current_user():
            raise tornado.HTTPError(404)

        self.set_header('Content-Type', 'text/plain')

        photo_uuid = tornado.escape.url_unescape(self.get_argument('photoUuid'), encoding='utf-8', plus=True)
        photo = DBRequester().GetPhotoByUuid(photo_uuid)

        self.write(photo.photo)
        self.finish()
