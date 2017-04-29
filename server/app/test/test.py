# TODONT
import sys
sys.path.insert(0, '/vendor') 

import os
import re

def get_sys_name():
 for key in os.environ:
   if re.search(r"_NAME", key):
     v = os.environ[key]
     return v[1:v.find('_')].upper()

sys_name = get_sys_name()

import databacon

databacon.connect({
  'shards': [{
    'shard': 0,
    'count': 4,
    'host': os.environ['%s_DB_1_PORT_5432_TCP_ADDR' % sys_name],
    'port': os.environ['%s_DB_1_PORT_5432_TCP_PORT' % sys_name],
    'user': 'dex',
    'password': '',
    'database': 'dex',
  }],
  'lookup_insertion_plans': [[(0, 1)]],
  'shard_bits': 8,
  'digest_key': 'super secret',
})


from schema import User, Event


users = [User() for u in range(20)]
host = users.pop()
event = Event('paris accords', host, users)
