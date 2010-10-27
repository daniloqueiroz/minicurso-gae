from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import model
import os

def render(out, tpl_name, values={}):
    path = os.path.join(os.path.dirname(__file__),tpl_name) 
    out.write(template.render(path, values))

class ShowEvent(webapp.RequestHandler):
    def get(self, ev_name):
        ev = model.get_event_by_name(ev_name)
        render(self.response.out, "event.html", {"event": ev})

class ListEvents(webapp.RequestHandler):
    def get(self):
        # pegar evento
        render(self.response.out, "events.html")
    

class CreateEvent(webapp.RequestHandler):
    def get(self):
        render(self.response.out, "createform.html")
    def post(self):
        ev_name = self.request.get('name')
        ev_locale = self.request.get('locale')
        model.create_new_event(ev_name, ev_locale)
        self.redirect("/event/" + ev_name)


application = webapp.WSGIApplication([('/event/create', CreateEvent),
                                      ('/events',ListEvents),
                                      ('/event/(.*)', ShowEvent)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
