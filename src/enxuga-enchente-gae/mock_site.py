import os
import cgi
import datetime
import wsgiref.handlers

try:
    import json
except ImportError:
    import simplejson as json

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import *
from google.appengine.ext.webapp.util import login_required

class AddProblemPage(webapp.RequestHandler):
    @login_required
    def get(self):
        self.response.out.write(template.render(os.path.dirname(__file__) + "/templates/add_problem.html", {"user":users.get_current_user()}))


class AddCommentPage(webapp.RequestHandler):
    @login_required
    def get(self):
        self.response.out.write(template.render(os.path.dirname(__file__) + "/templates/add_comment.html", {"user":users.get_current_user()}))


application = webapp.WSGIApplication([('/mock/add_problem', AddProblemPage),
                                      ('/mock/add_comment', AddCommentPage)], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
