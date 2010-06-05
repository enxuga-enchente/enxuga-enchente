#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cgi
import datetime
import wsgiref.handlers

import simplejson as json

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

from models import * 


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Funcionar, funciona')


class ManyProblemsPage(webapp.RequestHandler):
    def get(self):
        pass


class OneProblemPage(webapp.RequestHandler):
    
    def get(self):
        return json.JSONEncoder().encode(self, Problem.get(self.request.GET.get("id")))

    def post(self):
        problem = Problem(author=self.request.user,
                          geolocation=self.request.POST.get("geolocation"),
                          description=self.request.POST.get("description"))
        problem.put()
        
        
class PhotoPage(webapp.RequestHandler):
    def get(self):
        return json.JSONEncoder().encode(self, Photo.get(self.request.GET.get("id")))

    def post(self):
        image = self.request.POST.get("photo")
        
        photo = Photo(problem=self.request.POST.get("problem_id"),
                      author=users.get_current_user(),
                      description=self.request.POST.get("description"))
                      
        photo.put()


class CommentPage(webapp.RequestHandler):
    pass
        
application = webapp.WSGIApplication([('/problems', ManyProblemsPage),
                                      ('/problem', OneProblemPage),
                                      ('/photo', PhotoPage)], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
