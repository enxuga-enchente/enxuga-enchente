import unittest

from google.appengine.ext.db import GeoPt

from models import *

class ProblemTest(unittest.TestCase):
    
    def setUp(self):
        problem = Problem(author=None,
                  geolocation=GeoPt(1,1),
                  description="qwerty")
        problem.put()
        
        photo = Photo(author=None,
                      problem=problem,
                      description="asd")
        photo.put()
        
    
    def test_add_problem(self):
        problem = Problem(author=users.User("test"),
                          geolocation=GeoPt(1,2),
                          description="TESTE")
        problem.put()

        self.assertEquals(Problem.all().count(), 2)
        
        
        