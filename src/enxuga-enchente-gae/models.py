# -*- coding:utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users

    
class Problem(db.Model):
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    geolocation = db.GeoPtProperty()
    description = db.TextProperty()
    closed = db.BooleanProperty(default=False)
    votes = db.IntegerProperty()

    # TODO: Move these 3 methods into a mixin (called "Votable"?)
    def vote(self, author, vote):
        v = ProblemVote(problem = self, author = author, vote = vote)
        v.put()
        self.votes_total += vote
        self.put()

    def vote_up(self, author):
        self.vote(author = author, vote = +1)

    def vote_down(self, author):
        self.vote(author = author, vote = +1)


class Photo(db.Model):
    """Informações da foto do problema"""
    
    problem = db.ReferenceProperty(Problem)
    author = db.UserProperty()

    description = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
   
    
class Comment(db.Model):
    """
    a comment made on a problem
    """
    
    author = db.UserProperty()
    problem = db.ReferenceProperty(Problem)
    
    text = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
    def vote(self, author, vote):
        v = CommentVote(comment = self, author = author, vote = vote)
        v.put()
        self.votes_total += vote
        self.put()

    def vote_up(self, author):
        self.vote(author = author, vote = +1)

    def vote_down(self, author):
        self.vote(author = author, vote = +1)

    
class ProblemVote(db.Model):
    """
    up/down vote for a problem
    """
    
    problem = db.ReferenceProperty(Problem)
    author = db.UserProperty()
    vote = db.IntegerProperty()
    
    
class CommentVote(db.Model):
    """
    up/down vote for a comment
    """
    
    comment = db.ReferenceProperty(Comment)
    user = db.UserProperty()
    vote = db.IntegerProperty()
    
    
