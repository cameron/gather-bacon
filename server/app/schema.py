import databacon as db

class Gather(db.Node):
  active_users = db.relation('User')
  

class User(db.Node):
  schema = str
  flags = db.flags()
  flags.is_active = db.flag.bool()
  phone = db.lookup.alias()
  token = db.prop(str)
  friends = db.relation('User')
  friends.flags.muted = db.flag.bool()
  hosting = db.relation('Event')
  invites = db.relation('Event')
  lists = db.relation('List')
  feed = db.relation('FeedEntry')

  def json(self):
    return {'id': self.guid, 'name': self.value }


class Event(db.Node):
  schema = str
  host = db.relation(User.hosting)
  invitees = db.relation(User.invites)

  def json(self):
    return {'id': self.guid, 'title': self.value }
  

class List(db.Node):
  schema = str
  user = db.relation(User.lists)
  users = db.relation(User)


class FeedEntry(db.Node):
  schema = str
  user = db.relation(User.feed)
  
  def json(self):
    return { 'id': self.guid, 'text': self.value }
