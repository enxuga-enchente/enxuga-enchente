#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cgi
import datetime
import wsgiref.handlers
import sys

from django.utils import simplejson as json

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp import blobstore_handlers
from models import * 

import pdb

class PhotoUploader(webapp.RequestHandler):
    def get(self):
        path = 'templates/add_photo.html'
        
        template_values = {'problems': Problem.all() }
        self.response.out.write(template.render(path, template_values))

    def post(self):
        # for attr in ('stdin', 'stdout', 'stderr'):
        #     setattr(sys, attr, getattr(sys, '__%s__' % attr))
        # pdb.set_trace()

        problem = Problem.get_by_id(int(self.request.get('problem_id')))
        photo = Photo(problem = problem)
        photo.image = db.Blob(self.request.get('photo'))
        photo.put()

application = webapp.WSGIApplication([('/admin/add_photo.html', PhotoUploader )], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
