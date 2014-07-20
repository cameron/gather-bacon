#!/usr/bin/env python
# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

from graphite_api.app import app as graphite_api


def app(environ, original_start_response):
    def start_response(status, headers):
        for key, value in headers:
            if key.lower() == 'access-control-allow-origin':
                break
        else:
            #FIXME: kind of a no-no
            headers.append(('Access-Control-Allow-Origin', '*'))
        return original_start_response(status, headers)

    return graphite_api(environ, start_response)
