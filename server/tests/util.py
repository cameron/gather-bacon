from requests import Session
from functools import partial

s = Session()
def req(method, path, raw=False, **data):
  kwargs = { 'json': data }
  if method == 'GET':
    kwargs = { 'params': data }
  res = s.request(method, 'http://localhost:8080/api/%s' % path, **kwargs)
  if raw:
    return res
  if res.text:
    return res.json()

get = partial(req, 'GET')
post = partial(req, 'POST')
delete = partial(req, 'DELETE')  
