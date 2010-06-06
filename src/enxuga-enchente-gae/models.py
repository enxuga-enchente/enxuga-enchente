# -*- coding:utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users

    
class Problem(db.Model):
    author = db.UserProperty()
    title = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    geolocation = db.GeoPtProperty()
    description = db.TextProperty()
    closed = db.BooleanProperty(default=False)
    votes_total = db.IntegerProperty(default=0)

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

    def comment(self, author, text):
        comment = Comment(problem=self, author=author, text=text)
        comment.put()

    def serialize(self):
        return {"author":str(self.author),
                "photos":Photo.serialize_set(self.photo_set),
                "comments":Comment.serialize_set(self.comment_set),
                "geolocation":(self.geolocation.lat, self.geolocation.lon),
                "description":self.description}

    @classmethod
    def serialize_set(cls, set):
        return [obj.serialize() for obj in set]


class Photo(db.Model):
    """Informações da foto do problema"""
    
    problem = db.ReferenceProperty(Problem)
    author = db.UserProperty()
    image = db.BlobProperty()

    description = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    def serialize(self):
        return {"problem_id":self.problem.key().id(),
                "author":str(self.author),
                "image":self.image,
                "description":self.description,
                "date":self.date.strftime("%H:%M - %d/%m/%Y")}

    @classmethod
    def serialize_set(cls, set):
        return [obj.serialize() for obj in set]
    
    
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

    def serialize(self):
        return {"problem_id":self.problem.key().id(),
                "author":str(self.author),
                "text":self.text,
                "date":self.date.strftime("%H:%M - %d/%m/%Y")}

    @classmethod
    def serialize_set(cls, set):
        return [obj.serialize() for obj in set]

    
class ProblemVote(db.Model):
    """
    up/down vote for a problem
    """
    
    problem = db.ReferenceProperty(Problem)
    author = db.UserProperty()
    vote = db.IntegerProperty()

    def serialize(self):
        return {"problem_id":self.problem.key().id(),
                "author":str(self.author),
                "vote":self.vote}

    @classmethod
    def serialize_set(cls, set):
        return [obj.serialize() for obj in set]

    
    
class CommentVote(db.Model):
    """
    up/down vote for a comment
    """
    
    comment = db.ReferenceProperty(Comment)
    user = db.UserProperty()
    vote = db.IntegerProperty()
    
    def serialize(self):
        return {"comment_id":self.comment.key().id(),
                "author":self.author.email,
                "vote":self.vote}

    @classmethod
    def serialize_set(cls, set):
        return [obj.serialize() for obj in set]    
