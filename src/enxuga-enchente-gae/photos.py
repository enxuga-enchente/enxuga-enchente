#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cgi
import datetime
import wsgiref.handlers

import json

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import * 

class PhotoHandler(webapp.RequestHandler):
    def get(self, photo_id):
        photo = Photo.get('ID=', photo_id)
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(photo.image)


application = webapp.WSGIApplication([('photos/(.*)', PhotoHandler),], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
