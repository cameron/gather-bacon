import random, time
from util import get, post, delete 


def create_user(start_session=True):
  phone = ''.join(str(random.randint(0,9)) for x in range(10))
  name = ''.join(chr(random.randint(65, 91)) for x in range(10))
  return post('user', phone=phone, start_session=start_session, name=name)

#
# "tests"
#

# create a user
uid, token, phone = create_user()
assert token is not None

# verify logged in
logged_in_uid = get('session')
assert uid == logged_in_uid

# log out
delete('session')
assert get('session', raw=True).status_code == 401

# log back in
post('session', phone=phone, token=token)
assert get('session') == uid

# make some friends
users = [create_user(start_session=False) for u in range(10)]
[post('user/friends/%s' % uid) for uid, t, p in users]
assert len(get('user/friends')) == 10

# mute a friend
post('user/friends/%s/mute' % users[0][0])
assert len(get('user/friends/muted')) == 1

# host some events
num_events = 1
for x in range(num_events):
  eid = post('event', title='fun times')
  assert int(eid)

  # update the event (we could have done this in the post() above, too)
  post('event/%s' % eid, add_invitees=[uid for uid, t, p in users])

  # get the event details and verify the invite list
  assert len(get('event/%s/' % eid)['invitees']) == len(users)

# verify that the user is hosting num_events events
assert len(get('user/hosting')) == num_events

# verify that an invited user has an invite and a feed entry
delete('session')
post('session', phone=users[0][2], token=users[0][1])
assert len(get('user/invites')) == num_events
assert len(get('user/feed')) == num_events
