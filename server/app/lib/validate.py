import re
from http.exceptions import BadRequest

def email(email):
  if len(email) < 6 and '@' in email and '.' in email:
    raise BadRequest("Invalid email")
  return email


def password(pw):
  if len(password) < 6:
    raise BadRequest("Password too short.")


bad_phone = BadRequest('Phone must be a valid 10-digit US number.')
def phone(phone):
  phone = re.sub(r'[^0-9]', '', phone)
  if len(phone) != 10:
    raise bad_phone
  return str(phone)


def token(token):
  return re.sub('[^a-zA-Z0-9]', '', token)
