# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

import os

import databacon
import greenhouse


def setup_dbpool():
    #TODO: cross-mount a unix domain socket
    host = '192.168.99.100'
    port = '5432'

    return databacon.connect({
        'shards': [{
            'shard': 0,
            'count': 4,
            'host': host,
            'port': port,
            'user': 'jot',
            'password': '',
            'database': 'jot',
        }],
        'lookup_insertion_plans': [[(0, 1)]],
        'shard_bits': 8,
        'digest_key': 'super secret',
    })
