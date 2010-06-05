# -*- coding:utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

