#! /usr/bin/env python

# ug
import sys
sys.path.insert(0, '/vendor')
sys.path.insert(0, '/app')


from greenhouse.scheduler import schedule

from app import app
from schema import User, Event, FeedEntry
from lib.http import (
  get,
  post,
  delete,
  put,
  init_session,
  clear_session,
  req,
  optional
)
from lib.http.exceptions import Unauthorized, NotFound, BadRequest
from lib import validate
from lib import gen_token



@post('/user', {
  'phone': validate.phone,
  optional('name'): str,
  optional('start_session'): bool
}, public=True)
def create_user(phone=None, name=None, start_session=True):
  result = User.by_phone(phone)
  if result:
    raise BadRequest("Phone in use")
  
  user = User()
  user.value = name
  user.save()
  user.phone(phone)
  token = gen_token(phone)
  user.token(token)
  if start_session:
    init_session(user)
  return [user.guid, token, phone]


@post('/session', {
  'phone': validate.phone,
  'token': validate.token
}, public=True)
def login(phone=None, token=None):
  user = User.by_phone(phone)
  if not user:
    raise NotFound('User not found')

  if token != user.token().value:
    raise Unauthorized()

  init_session(user)
  return user.guid


@get('/session')
def check_session():
  return req.user.guid


@delete('/session')
def logout():
  clear_session()


@post('/user/friends/<int:fid>')
def add_friend(fid):
  req.user.friends.add(guid=fid)
  return 'ok'


@post('/user/friends/<int:fid>/mute')
def mute_friend(fid):
  edge = req.user.friends.get(guid=fid)
  edge.flags.muted = True
  edge.flags.save()
  return 'ok'


@get('/user/friends/muted')
def get_muted_friends():
  return [node.guid for edge, node in req.user.friends(nodes=True) if edge.flags.muted]


@get('/user/friends')
def friends():
  return [node.guid for edge, node in req.user.friends(nodes=True)]


@get('/user/hosting')
def user_hosting():
  return [node.guid for edge, node in req.user.hosting(nodes=True)]


@get('/user/invites')
def user_invites():
  return [node.guid for edge, node in req.user.invites(nodes=True)]


@get('/user/feed')
def user_feed():
   return [node.json() for edge, node in req.user.feed(nodes=True)]

@get('/user/list')
def lists():
  return [[node.guid for edge, node in node.users(nodes=True)] for
          edge, node in req.user.lists(nodes=True)]

@post('/event', {
  'title': str,
  optional('invitees'): [int]
})
def create_event(title=None, invitees=None):
  event = Event()
  event.host.add(req.user)
  update_event(None,
               event=event,
               title=title,
               add_invitees=invitees,
               _apply_json_spec=False) 
  return event.guid


@post('/event/<int:eid>', {
  optional('add_invitees'): [int],
  optional('rm_invitees'): [int],
  optional('title'): str
})
def update_event(
    eid,
    add_invitees=None,
    rm_invitees=None,
    title=None,
    event=None):
  if not event:
    event = Event.by_guid(eid)

  if title:
    event.value = title
    event.save()

  for uid in (add_invitees or []):
    event.invitees.add(guid=uid)
    entry = FeedEntry()
    entry.value = '%s invited you to %s' % (req.user.value, event.value)
    entry.save()
    User(dh={'id': uid}).feed.add(entry)

  for uid in (rm_invitees or []):
    event.invitees.remove(guid=uid)

  

@get('/event/<int:eid>/')
def get_event(eid):
  event = Event.by_guid(eid)
  host = list(event.host(nodes=True))[0][1]
  return {
    'id': event.guid,
    'host': host.guid,
    'invitees': [node.guid for rel, node in event.invitees(nodes=True)]
  }


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
