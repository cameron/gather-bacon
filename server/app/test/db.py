import os
import databacon

def get_sys_name():
 for key in os.environ:
   if re.search(r"_NAME", key):
     v = os.environ[key]
     return v[1:v.find('_')].upper()

sys_name = get_sys_name()

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
