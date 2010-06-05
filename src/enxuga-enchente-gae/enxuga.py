#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

from models import * 


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Funcionar, funciona')


class Guestbook(webapp.RequestHandler):
    def post(self):
        self.redirect('/')


application = webapp.WSGIApplication([('/', MainPage),
                                      ('/sign', Guestbook)], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
