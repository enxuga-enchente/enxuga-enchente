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


class ManyProblemsPage(webapp.RequestHandler):
    def get(self):
        return self.response.out.write(json.JSONEncoder().encode({"result":Problem.serialize_set(Problem.all())}))


class OneProblemPage(webapp.RequestHandler):
    
    def get(self):
        return json.JSONEncoder().encode(Problem.get(self.request.GET.get("id")))

    def post(self):
        geopt = db.GeoPt(self.request.POST.get("geolocation_lat"), self.request.POST.get("geolocation_lon"))
        
        problem = Problem(author=users.get_current_user(),
                          geolocation=geopt,
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
    def post(self):
        Problem.get(self.request.POST.get("problem_id")).comment(author=self.get_current_user(),
                                                                 text=self.request.POST.get("text"))
        
        
class ProblemVotePage(webapp.RequestHandler):
    def post(self):
        Problem.get(self.request.POST.get("problem_id")).vote(author=self.get_current_user(),
                                                              vote=self.request.POST.get("vote"))


class CommentVotePage(webapp.RequestHandler):
    def post(self):
        Comment.get(self.request.POST.get("comment_id")).vote(author=self.get_current_user(),
                                                              vote=self.request.POST.get("vote"))


application = webapp.WSGIApplication([('/problems', ManyProblemsPage),
                                      ('/problem', OneProblemPage),
                                      ('/problem_vote', ProblemVotePage),
                                      ('/photo', PhotoPage),
                                      ('/comment', CommentPage),
                                      ('/comment_vote', CommentVotePage)], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
