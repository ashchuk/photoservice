#!/usr/bin/env python
import tornado.web

from wsgi.handlers.BaseHandler import BaseHandler
from wsgi.handlers.PhotoHandlers import AddPhoto, GetRandomPhoto, GetPhotoByUuid, GetPhotos, GetBase64ImageByPhotoUuid
from wsgi.handlers.UserHandlers import AddUser, GetUser, UpdateUser, GetUserAvatar
from wsgi.handlers.LoginHandlers import LoginHandler, LogoutHandler, DropDBHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self, message=""):
        self.render('index.html')


class NotFoundRequestHandler(BaseHandler):
    def get(self):
        self.set_status(404)
        self.render('index.html')

handlers = [(r'/', MainHandler,),

            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),

            (r'/registration', AddUser),
            (r'/getuser', GetUser),
            (r"/getuseravatar", GetUserAvatar),
            (r"/updateuser", UpdateUser),

            (r"/addphoto", AddPhoto),
            (r"/getrandomphoto", GetRandomPhoto),
            (r"/getphoto", GetPhotoByUuid),
            (r"/getimage", GetBase64ImageByPhotoUuid),
            (r"/getphotos", GetPhotos),

            (r"/.*", NotFoundRequestHandler),
            ]
