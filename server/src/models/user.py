import databason as db

class User(db.Node):
  email = db.lookup.alias()
  email.flags.verification_status = db.flag.enum('unsent',
                                                 'sent',
                                                 'resent',
                                                 'confirmed')
  password = db.prop(unicode)
