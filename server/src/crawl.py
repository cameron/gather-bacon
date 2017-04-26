import sys
sys.path.insert(0, '/vendor')
print sys.path

from lib import dev
from lib import resources
resources.setup_dbpool()

from models.domain import Domain
d = Domain.by_url('http://news.ycombinator.com')
# left off debugging why _meta is empty here
print d.wwws.of_type._meta

from models.www import WWW
www = WWW.singleton()
print www.domains.of_type._meta 


#Page.by_url('http://news.ycombinator.com').remove()
#page = www.add_url('http://news.ycombinator.com')

from models.crawler import Crawler
Crawler.wake_or_create().crawl()

# TODO
#
# benchmarks/
# - demonstrate linear scalability
#   - runs: 1,10,100, 1000?/ node/shards
#   - total cost per run
#
# deploy/
# - kubernetes!
# - colocate on one machine api/db?
#   - the api layer might sit well on the same machine as a postgres instance:
#     the db would max out cpu and disk while api maxes out network
#
