import tornado.web
import os
import functools

def cacheProtectorDecorator(method):
    @tornado.web.authenticated
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')
        return method(self, *args, **kwargs)
    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("userUuid")
