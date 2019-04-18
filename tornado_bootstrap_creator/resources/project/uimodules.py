#!/usr/bin/env python

import os
import tornado.web

class RoutesMenu(tornado.web.UIModule):
    def render(self, name):
        return self.render_string(os.path.join('ui', 'menu.html'), name = name)