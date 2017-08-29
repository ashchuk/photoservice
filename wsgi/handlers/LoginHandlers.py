from datetime import datetime
import jsonpickle
from wsgi.handlers.BaseHandler import *


class LoginHandler(BaseHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        self.set_header('Content-Type', 'application/json')

        user = DBRequester().GetUserByCredentials(
            self.get_argument("email"),
            self.get_argument("password")
        )

        if not user:
            raise tornado.HTTPError(401)

        if not self.get_cookie("userUuid"):
            self.set_secure_cookie("userUuid", user.uuid)

        self.write(jsonpickle.encode(user, unpicklable=False))


class LogoutHandler(BaseHandler):
    @cacheProtectorDecorator
    def get(self):
        self.clear_cookie("userUuid")
        self.redirect(r'/')

