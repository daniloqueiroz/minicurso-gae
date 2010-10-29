# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import google.appengine.api.users as users
from google.appengine.ext.webapp.util import login_required
import os

class Open(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

class Close(webapp.RequestHandler):
    @login_required
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

class Post(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            params = { 'name' : self.request.get('name')}        
            path = os.path.join(os.path.dirname(__file__), 'index.html')
            self.response.out.write(template.render(path, params))


'''Aplicação / Mapeamentos'''
application = webapp.WSGIApplication([('/open', Open),
                                      ('/close', Close),
                                      ('/post', Post)
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
