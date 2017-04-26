import sys
sys.path.insert(0, '/vendor')
print sys.path

from lib import dev
from lib import resources
resources.setup_dbpool()

from models.domain import Domain
Domain.by_url('http://news.ycombinator.com')

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
