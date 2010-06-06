#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cgi
import datetime
import wsgiref.handlers

from django.utils import simplejson as json

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
        return json.JSONEncoder().encode(Problem.get(self.request.get("id")))

    def post(self):
        geopt = db.GeoPt(self.request.get("geolocation_lat"), self.request.get("geolocation_lon"))
        
        problem = Problem(author=users.get_current_user(),
                          geolocation=geopt,
                          description=self.request.get("description"))
        problem.put()
        
        
class PhotoPage(webapp.RequestHandler):
    def get(self):
        return json.JSONEncoder().encode(self, Photo.get(self.request.GET.get("id")))

    def post(self):
        image = self.request.get("photo")
        
        photo = Photo(problem=self.request.get("problem_id"),
                      author=users.get_current_user(),
                      description=self.request.get("description"))
        photo.put()


class CommentPage(webapp.RequestHandler):
    def post(self):
        Problem.get_by_id(int(self.request.get("problem_id"))).comment(author=users.get_current_user(),
                                                                       text=self.request.get("text"))
        
        
class ProblemVotePage(webapp.RequestHandler):
    def post(self):
        Problem.get_by_id(int(self.request.get("problem_id"))).vote(author=self.get_current_user(),
                                                              vote=self.request.get("vote"))


class CommentVotePage(webapp.RequestHandler):
    def post(self):
        Comment.get_by_id(int(self.request.get("comment_id"))).vote(author=self.get_current_user(),
                                                              vote=self.request.get("vote"))
class HomeJSONHandler(webapp.RequestHandler):
    def get(self):
        results = {}
        results['feed'] = [ {'date': p.date.strftime('%H:%M %d/%m/%Y'), 'problem_id': p.key().id(), 
                             'problemTitle': p.title,
                             'problemMedias': [ { 'mediaType': 'photo',
                                                  'mediaTitle': m.description,
                                                  'mediaUrl': 'http://enxuga-enchente.appspot.com/photos/%d' % m.key().id() } for m in p.photo_set ] } for p in Problem.all() ]
        self.response.out.write(json.JSONEncoder(indent = 4).encode(results))


application = webapp.WSGIApplication([('/problems', ManyProblemsPage),
                                      ('/problem', OneProblemPage),
                                      ('/problem_vote', ProblemVotePage),
                                      ('/photo', PhotoPage),
                                      ('/comment', CommentPage),
                                      ('/comment_vote', CommentVotePage),
                                      ('/home.json', HomeJSONHandler)], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
