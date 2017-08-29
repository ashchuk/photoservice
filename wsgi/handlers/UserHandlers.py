import jsonpickle

from wsgi.handlers.BaseHandler import *
from wsgi.logics.DBRequester import DBRequester, UserMissingError


class AddUser(BaseHandler):
    def get(self):
        self.render('registration.html')

    def post(self):
        email = tornado.escape.url_unescape(self.get_argument("email"), encoding='utf-8', plus=True)
        password = tornado.escape.url_unescape(self.get_argument("password"), encoding='utf-8', plus=True)
        nickname = tornado.escape.url_unescape(self.get_argument("nickname"), encoding='utf-8', plus=True)
        image = self.request.files['filearg'][0] if 'filearg' in self.request.files else None

        user = DBRequester().GetUserByCredentials(email, password)
        if user:
            self.write("User already exists")
            self.set_status(409)
            return

        user = DBRequester().AddUser(email=email,
                                     password=password,
                                     nickname=nickname,
                                     avatar_dict=image)

        self.clear_cookie("userUuid")
        self.set_secure_cookie("userUuid", user.uuid)
        self.write(jsonpickle.encode(user, unpicklable=False))


class UpdateUser(BaseHandler):
    def post(self):
        name_arg = self.get_argument("nickname", default=None, strip=False)
        nickname = tornado.escape.url_unescape(name_arg, encoding='utf-8', plus=True) if name_arg is not None else None

        image = self.request.files['filearg'][0] if 'filearg' in self.request.files else None

        try:
            user = DBRequester().UpdateUser(user_uuid=self.get_current_user().decode(encoding='utf-8'),
                                            nickname=nickname,
                                            avatar_dict=image)
            self.write(jsonpickle.encode(user, unpicklable=False))
        except UserMissingError as ex:
            self.write("User missing")
            self.set_status(404)


class GetUser(BaseHandler):
    def get(self):
        user_uuid = tornado.escape.url_unescape(self.get_argument("userUuid"), encoding='utf-8', plus=True)
        user = DBRequester().GetUserByUuid(user_uuid)
        if not user:
            self.set_status(404)
            self.write("User missing")

        self.set_header('Content-Type', 'application/json')
        self.write(jsonpickle.encode(user, unpicklable=False))


class GetUserAvatar(BaseHandler):
    def get(self):
        user_uuid = tornado.escape.url_unescape(self.get_argument("userUuid"), encoding='utf-8', plus=True)
        user = DBRequester().GetUserByUuid(user_uuid)

        self.set_header('Content-Type', 'text/plain')

        if user:
            self.write(user.avatar)
