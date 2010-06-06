# -*- coding:utf-8 -*-

import cgi
import datetime
import wsgiref.handlers

import json

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

from google.appengine.ext.db import GeoPt
from models import *
from django.contrib.auth.decorators import login_required

class CreateFixtures(webapp.RequestHandler):
    def get(self):
        problem = Problem(author=None,
                          geolocation=GeoPt(1,1),
                          description="qwerty")
        problem.put()
        
        photo = Photo(author=None,
                      problem=problem,
                      description="asd")

        photo.put()

        self.response.out.write("fixtures created")


application = webapp.WSGIApplication([('.*', CreateFixtures)], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
