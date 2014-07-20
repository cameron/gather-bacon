# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

import os

import datahog
import greenhouse
import statistician

redis = greenhouse.patched("redis")


redispool = None
dbpool = None

def setup_redispool():
    global redispool

    #TODO: cross-mount a unix domain socket
    if "REDIS_PORT_6379_TCP_ADDR" in os.environ:
        host = os.environ["REDIS_PORT_6379_TCP_ADDR"]
        port = os.environ["REDIS_PORT_6379_TCP_PORT"]

    redispool = redis.ConnectionPool(host=host, port=port, db=0,
            socket_timeout=1.0)

def get_redis():
    return redis.Redis(connection_pool=redispool)

def setup_dbpool():
    global dbpool

    #TODO: cross-mount a unix domain socket
    if "DB_PORT_5432_TCP_ADDR" in os.environ:
        host = os.environ['DB_PORT_5432_TCP_ADDR']
        port = os.environ['DB_PORT_5432_TCP_PORT']

    dbpool = datahog.GreenhouseConnPool({
        'shards': [{
            'shard': 0,
            'count': 4,
            'host': host,
            'port': port,
            'user': 'legalease',
            'password': '',
            'database': 'legalease',
        }],
        'lookup_insertion_plans': [[(0, 1)]],
        'shard_bits': 8,
        'digest_key': 'super secret',
    })
    dbpool.start()
    if not dbpool.wait_ready(2.0):
        raise Exception("postgres connection timeout")


# statsd = statistician.Client(
#         host=os.environ['STATSD_PORT_8125_UDP_ADDR'],
#         port=int(os.environ['STATSD_PORT_8125_UDP_PORT']),
#         prefix='server')

def setup_statsd():
    statistician._sock = None
