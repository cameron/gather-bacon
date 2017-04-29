import sys
import time
import json
import functools

from flask import request as flask_req, got_request_exception, session

from exceptions import (
  BadJson,
  Unauthorized,
  HTTPException,
  InternalServerError,
  UnrecognizedParameters
)
from app import app
from schema import User


__ALL__ = [
  'get',
  'post',
  'delete',
  'put',
  'require_json',
  'is_logged_in_as',
  'require_login',
  'optional',
  'init_session',
  'json_spec',
  'req',
  'clear_session'
]


class Request(object):
  ''' Wrapper for Flask.request to force request.json to appear
  as a dictionary if None.'''

  def __getattr__(self, name):
    if name == 'json':
      return flask_req.json or {}
    return getattr(flask_req, name)

req = Request()


default_headers = {
  'Content-type': 'application/json',
}
BODY_AND_CODE = 2
BODY_CODE_AND_HEADERS = 3
def return_json(endpoint):
  ''' Decorate endpoint to return JSON with proper headers. '''
  @functools.wraps(endpoint)
  def endpoint_returns_json(*args, **kwargs):
    
    code = 200
    headers = default_headers
    response = endpoint(*args, **kwargs)

    if type(response) is tuple:
      if len(response) == BODY_AND_CODE:
        response, code = response
      elif len(response) == BODY_CODE_AND_HEADERS:
        response, code, headers = response
        for header, val in default_headers.iteritems():
          headers.setdefault(header, val)

    return (json.dumps(response), code, headers)
  return endpoint_returns_json


@app.errorhandler(Exception)
@return_json
def errorhandler(e):
  if issubclass(type(e), HTTPException):
    return {'msg': e.msg}, e.response_code
  import traceback
  traceback.print_exc()
  return {'msg': 'internal server error'}, 500


def is_logged_in_as(guid):
  if not logged_in_guid() == guid:
    raise Unauthorized
  return True


def logged_in_guid():
  guid = session.get('guid')
  if guid and session.get('expires', -1) > time.time():
    return guid
  return None


def require_login(fn):
  @functools.wraps(fn)
  def endpoint_requires_login(*args, **kwargs):
    guid = logged_in_guid()
    if guid:
      req.user = User.by_guid(guid)
      return fn(*args, **kwargs)
    raise Unauthorized()
  return endpoint_requires_login


class optional(object):
  def __init__(self, name):
    self.name = name


def apply_json_spec(param, spec, keypath=''):
  ''' E.g.,
  apply_json_spec(json, {
    'email': str                 # validate using a type (will NOT coerce, except unicode->str)
    'email': None                # no validation, but key is required
    'email': validator           # custom validator/converter,
    'list_o_ints': [int]         # apply int as a validator to all elements
    'user': {'some': 'thing'}    # a sub-spec 
    optional('email'): validator # optional key
  })
  '''

  # No validation
  if spec is None:
    return param

  # Basic type validation (no coercion)
  if type(spec) is type:
    if type(param) is unicode and spec is str:
      param = str(param)
    if type(param) is not spec:
      raise BadJson(spec, param, keypath)
    return param

  # Custom validator/converter
  if callable(spec):   
    return spec(param) 

  # List
  if type(spec) is list:
    if type(param) is not list:
      raise BadJson(list, param, keypath)
    if len(spec) == 1:
      for idx,val in enumerate(param):
        param[idx] = apply_json_spec(val, spec[0], keypath='%s[%s]' % (keypath, idx))
    return param

  # Only remaining acceptable spec is a dict, so guard against programmer error
  if type(spec) is not dict:
    raise InternalServerError()

  # Dictionary
  unspecified_keys = param.keys()
  for key, key_spec in spec.iteritems():
    key_type = type(key)
    if key_type is optional:
      key = key.name
    key in unspecified_keys and unspecified_keys.remove(key)
    try:
      param[key] = apply_json_spec(param[key], key_spec, keypath + key)
    except KeyError:
      if key_type is not optional:
        raise BadJson(spec, param, keypath)

  if unspecified_keys:
    raise UnrecognizedParameters(unspecified_keys)

  return param


def json_spec(spec=None):
  def json_spec_dec(endpoint):
    @functools.wraps(endpoint)
    def endpoint_accepts_json(*args, **kwargs):
      if kwargs.pop('_apply_json_spec', True):
        if req.json:
          print req.json
          kwargs.update(apply_json_spec(req.json, spec))
      return endpoint(*args, **kwargs)
    return endpoint_accepts_json
  return json_spec_dec


def init_session(user):
  session['guid'] = user.guid
  session['expires'] = time.time() + 3600*24*30


def clear_session():
  del session['guid']
  del session['expires']


def method_route_decorator_factory(methods):
  ''' Returns a decorator that accepts a path argument and supplies the
  provided `methods` to flask.App.add_url_rule.
  
  Returned decorators also accept a `spec` kwarg, a dictionary that 
  will be used to validate request.json. Intended for POST methods. See
  apply_json_spec() above.

  '''

  methods = type(methods) is str and [methods] or methods
  def method_route_decorator_args(path, spec=None, public=False):
    def method_route_decorator(endpoint):
      if not public:
        endpoint = require_login(endpoint)
      wrapper = return_json(endpoint)
      if json_spec:
        wrapper = json_spec(spec)(endpoint)
      wrapper = return_json(wrapper)
      endpoint.__name__ = endpoint.__name__ + '-'
      functools.update_wrapper(wrapper, endpoint)
      app.add_url_rule('/api' + path, wrapper.__name__, wrapper, methods=methods)
      return wrapper
    return method_route_decorator
  return method_route_decorator_args


get = method_route_decorator_factory('GET')
post = method_route_decorator_factory('POST')
delete = method_route_decorator_factory('DELETE')
put = method_route_decorator_factory('PUT')
