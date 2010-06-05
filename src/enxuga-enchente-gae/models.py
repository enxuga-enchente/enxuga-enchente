# -*- coding:utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users

    
class Problem(db.Model):
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
    closed = db.BooleanProperty(default=False)


class Photo(db.Model):
    """Informações da foto do problema"""
    
    problem = db.ReferenceProperty(Problem)
    author = db.UserProperty()
    
    db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
    geolocation = db.GeoPtProperty()
    
    
class Comment(db.Model):
    """Comentário relacionado a um problema"""
    
    photo = db.ReferenceProperty(Problem)
    
    
class Vote(db.Model):
    """Voto para um problema"""
    
    problem = db.ReferenceProperty(Problem)
    user = db.UserProperty()
    vote = db.IntegerProperty()
    
