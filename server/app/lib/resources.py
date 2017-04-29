# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

import os

import databacon
import greenhouse


sys_name = None
for key, val in os.environ.items():
    if key.endswith('_NAME'):
        sys_name = val[1:val.find('_')].upper()
        break

def setup_dbpool():
    #TODO: cross-mount a unix domain socket 
    host = os.environ['%s_DB_1_PORT_5432_TCP_ADDR' % sys_name]
    port = os.environ['%s_DB_1_PORT_5432_TCP_PORT' % sys_name]

    return databacon.connect({
        'shards': [{
            'shard': 0,
            'count': 4,
            'host': host,
            'port': port,
            'user': 'dex',
            'password': '',
            'database': 'dex',
        }],
        'lookup_insertion_plans': [[(0, 1)]],
        'shard_bits': 8,
        'digest_key': 'super secret',
    })
