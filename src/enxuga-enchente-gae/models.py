# -*- coding:utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users

    
class Problem(db.Model):
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    geolocation = db.GeoPtProperty()
    description = db.TextProperty()
    closed = db.BooleanProperty(default=False)


class Photo(db.Model):
    """Informações da foto do problema"""
    
    problem = db.ReferenceProperty(Problem)
    author = db.UserProperty()

    description = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
   
    
class Comment(db.Model):
    """Comentário relacionado a um problema"""
    
    user = db.UserProperty()
    problem = db.ReferenceProperty(Problem)
    
    text = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
    
class ProblemVote(db.Model):
    """Voto para um problema"""
    
    problem = db.ReferenceProperty(Problem)
    user = db.UserProperty()
    vote = db.IntegerProperty()
    
    
class CommentVote(db.Model):
    """Voto para o comentário"""
    
    comment = db.ReferenceProperty(Comment)
    user = db.UserProperty()
    vote = db.IntegerProperty()
    
    