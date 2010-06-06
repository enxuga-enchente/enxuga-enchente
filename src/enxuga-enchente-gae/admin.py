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

class PhotoUploader(webapp.RequestHandler):
    def get(self):
        path = 'templates/add_photo.html'
        
        template_values = {'problems': Problem.all() }
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([('/admin/add_photo.html', PhotoUploader )], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
