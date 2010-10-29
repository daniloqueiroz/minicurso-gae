# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import google.appengine.api.users as users
from google.appengine.ext.webapp.util import login_required

from datetime import datetime
import model
import os

def render(out, tpl_name, values={}):
    """
    Função auxiliar para evitar repetição de codigo
    
    Renderiza um template e imprime
    """
    path = os.path.join(os.path.dirname(__file__),tpl_name) 
    out.write(template.render(path, values))


class ShowEvent(webapp.RequestHandler):
    def get(self, ev_name):
        """
        Mostra um evento com o nome dado
        """
        ev = model.get_event_by_name(ev_name)
        render(self.response.out, "event.html", {"event": ev})


class ListEvents(webapp.RequestHandler):
    def get(self):
        """
        Lista eventos
    
        Proximos eventos ou 
        eventos antigos se old = true
        """ 
        old = bool(self.request.get('old'))
        if old:
            evs = model.get_past_events()
        else:
            evs = model.get_next_events()
        render(self.response.out, "list_events.html", {'events': evs, 'old': old})
    

class CreateEvent(webapp.RequestHandler):
    """
    Precisa estar logado para executar este handler
    """
    @login_required
    def get(self):
        """
        Redireciona para o form de criar eventos
        """
        render(self.response.out, "create_event.html")
        
    def post(self):
        """
        Cria um novo evento
        """
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            ev_name = self.request.get('name')
            ev_locale = self.request.get('locale')
            ev_date = self.request.get('date')
            ev_date = datetime.strptime(ev_date,'%d/%m/%y %H:%M')
            model.create_new_event(ev_name, ev_locale, ev_date)
            self.redirect("/event/" + ev_name)

class AddItem(webapp.RequestHandler):
    """
    Precisa estar logado para executar este handler
    """
    @login_required
    def get(self, ev_name):
        """
        Redireciona para o form de adicionar item
        """
        render(self.response.out, "add_item.html", {'event_name': ev_name})
        
    def post(self, ev_name):
        """
        Adiciona um novo item
        """
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            it_name = self.request.get('name')
            it_importance = self.request.get('importance')
            it_sponsor = self.request.get('sponsor')
            model.add_item_to_event(ev_name, it_name, it_importance, it_sponsor)
            self.redirect("/event/" + ev_name)


class Presence(webapp.RequestHandler):
    """
    Precisa estar logado para executar este handler
    """
    @login_required
    def get(self, ev_name):
        """
        Altera a participação do usuário em um dado evento
        """
        model.toggle_presence(ev_name)
        self.redirect("/event/" + ev_name)

'''Aplicação / Mapeamentos'''
application = webapp.WSGIApplication([('/event/create', CreateEvent),
                                      ('/',ListEvents),
                                      ('/event/(.*)/presence', Presence),
                                      ('/event/(.*)/add_item', AddItem),
                                      ('/event/(.*)', ShowEvent)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
