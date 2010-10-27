from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api.users import User

__importance = ["not important", "indispensable", "important"]

class Item(db.Model):
    item_name = db.StringProperty(required=True)
    importance = db.StringProperty(required=True, choices=set(__importance), default=__importance[0])
    sponsor = db.UserProperty(required=False)

class Event(db.Model):
    name = db.StringProperty(required=True)
    locale = db.StringProperty(required=True)
    host = db.UserProperty(required=True)
    participants = db.ListProperty(User)
    itens_to_bring = db.ListProperty(Item)
    
def create_new_event(ev_name, ev_locale):
    ev_host = users.get_current_user()
    event = Event(name=ev_name, locale=ev_locale, host=ev_host)
    event.participants = [ev_host]
    event.put()
    
def get_event_by_name(ev_name):
    return Event.all().filter("name =", ev_name).get()

def confirm_presense(ev_name):
    user = users.get_current_user()
    event = get_event_by_name(ev_name)
    event.participants.append(user)
    event.put()

def disconfirm_presense(ev_name):
    user = users.get_current_user()
    event = get_event_by_name(ev_name)
    if user in event.participants:
        event.participants.remove(user)
        event.put()
        
