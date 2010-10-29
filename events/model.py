# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api.users import User

from datetime import datetime


# Classes
class Event(db.Model):
    name = db.StringProperty(required=True)
    locale = db.StringProperty(required=True)
    host = db.UserProperty(required=True)
    date = db.DateTimeProperty(required=True)
    participants = db.ListProperty(User)

class Item(db.Model):
    event = db.ReferenceProperty(Event, collection_name='itens')
    name = db.StringProperty(required=True)
    importance = db.StringProperty(required=True, choices=set(["not important", "medium", "indispensable"]), default="not important")
    sponsor = db.StringProperty(required=True)

# business logic    
def create_new_event(ev_name, ev_locale, ev_date):
    ev_host = users.get_current_user()
    event = Event(name=ev_name, locale=ev_locale, host=ev_host, date=ev_date)
    event.participants = [ev_host]
    event.put()
    
def get_event_by_name(ev_name):
    return Event.all().filter("name =", ev_name).get()

def get_next_events():
    return Event.all().order('date').filter("date >", datetime.now()).fetch(100)

def get_past_events():
    return Event.all().order('-date').filter("date <", datetime.now()).fetch(100)

def add_item_to_event(ev_name, it_name, it_importance, it_sponsor):
    ev = get_event_by_name(ev_name)
    item = Item(event=ev, name=it_name, importance=it_importance, sponsor=it_sponsor)
    item.put()
    
def toggle_presence(ev_name):
    user = users.get_current_user()
    event = get_event_by_name(ev_name)
    if user in event.participants:
        event.participants.remove(user)
    else:
        event.participants.append(user)
    event.put()
        
