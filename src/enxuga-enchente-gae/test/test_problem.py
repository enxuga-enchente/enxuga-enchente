import unittest

from google.appengine.ext.db import GeoPt

from models import *

class ProblemTest(unittest.TestCase):
    
    def test_add_problem(self):
        problem = Problem(author=users.User("test"),
                          geolocation=GeoPt(1,2),
                          description="TESTE")
        problem.put()

        self.assertEquals(Problem.all().count(), 1)