import os
import random
import tornado.web
import json
import time
import hashlib

class BaseHandler(tornado.web.RequestHandler):

    layout = None
    name = None
    user_locale = None

    def initialize(self):
        lang = self.get_query_argument('lang', default = 'zh_CN')
        if lang:
            self.user_locale = tornado.locale.get(lang)
        return super(BaseHandler, self).initialize()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if user_id is not None:
            user_id = user_id.decode()
        if user_id is not None:
            self.set_secure_cookie('user', user_id, expires = time.time() + 3600)
            return user_id
        return None

    def render(self, template_name, **kwargs):
        kwargs['__name__'] = self.name
        user = self.get_current_user()
        kwargs['__user__'] = user
        if self.layout is None :
            return tornado.web.RequestHandler.render(self, template_name, **kwargs)
        else :
            kwargs['__content__'] = self.render_string(template_name, **kwargs)
            return tornado.web.RequestHandler.render(self, os.path.join('layouts', self.layout), **kwargs)


class IndexHandler(BaseHandler):

    layout = "default.html"
    name = 'index'

    @tornado.web.authenticated
    def get(self) :
        self.render('index.html')


class LoginHandler(BaseHandler):

    layout = "login.html"
    name = 'login'

    def get(self) :
        self.render('login.html', login_fail = False, next_goto = self.get_query_argument("next", None))

    def post(self) :
        user_id = self.get_body_argument("user_id")
        user_password = self.get_body_argument("user_password")
        next_goto = self.get_body_argument("next", self.get_query_argument("next", None))
        password_md5 = hashlib.md5()
        password_md5.update(user_password.encode('utf-8'))
        if user_id == self.application.settings["login_user"] and password_md5.hexdigest() == self.application.settings["login_password"] :
            self.set_secure_cookie("user", user_id)
            if next_goto is None :
                self.redirect("/index")
            else :
                self.redirect(next_goto)
        else :
            self.render('login.html', login_fail = True, next_goto = next_goto)


class LogoutHandler(BaseHandler) :

    layout = "login.html"
    name = 'login'

    def get(self) :
        self.clear_cookie("user")
        self.redirect("/login")

    def post(self) :
        self.get()


{% for handler, name in handlers.items() %}


class {{ handler }}(BaseHandler):
    layout = 'default.html'
    name = '{{name}}'

    @tornado.web.authenticated
    def get(self):
        self.render('{{name}}.html')


{% endfor %}