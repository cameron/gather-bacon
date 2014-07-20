# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

import functools
import json

import routing

from .storage import user, document
#from .resources import statsd

app = routing.App()

def api(func):
    """decorator for JSON API endpoints

    - JSONify return value
      - a tuple implies (error_code, payload)
    - CORS headers set to allow * (TODO: fix this)
    """
    @functools.wraps(func)
    def handler(http, *args, **kwargs):
        http.add_header('access-control-allow-origin', '*')
        http.add_header('content-type', 'application/json')
        return _invoke(func, (http,) + args, kwargs)
    return handler


def xdomain_iframe(func):
    """decorator for iframes that need to postMessage to the parent

    - JSONify return value, inject it in a <script> that postMessage's it up
      to the top frame
      - a tuple implies (error_code, payload)
    """
    @functools.wraps(func)
    def handler(http, *args, **kwargs):
        http.add_header('content-type', 'text/html')
        return "<script>top.postMessage(JSON.stringify(%s), '*')</script>" % \
                _invoke(func, (http,) + args, kwargs)
    return handler



def record(name):
    "decorator to record information about the request to statsd"
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            pass
            # with statsd.pipeline() as pipeline:
            #     with pipeline.timer(name):
            #         return func(*args, **kwargs)
            #     pipeline.incr(name)
        return decorated
    return decorator


@record('access.docs')
@app.get(r'^/docs$')
@api
def docs(http):
    return list(document.enumerate_docs(user.GLOBAL_UID))

@record('access.upload')
@app.post(r'^/upload$')
@xdomain_iframe
def process_upload(http):
    if 'upload' not in http.FILES:
        return 1, 'no file included'

    obj = http.FILES['upload']
#    statsd.time('upload.size', obj.content_length)
    name = obj.filename.encode('utf-8')
    path = document.store(user.GLOBAL_UID, name, obj.file)
    return {'name': name, 'path': path}


def _invoke(func, args, kwargs):
    error = None
    result = func(*args, **kwargs)
    if isinstance(result, tuple) and len(result) == 2:
        error, result = result
    return json.dumps({'error': error, 'data': result})
