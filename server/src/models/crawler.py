import greenhouse

import databacon as db
from domain import Domain
from www import WWW
from lib import profile

www = WWW.singleton()

class Crawler(db.Node):
  GREENLET_POOL_SIZE = 80000
  TIMEOUT = 10
  parent = WWW
  schema = int
  domains = db.relation(Domain)
  # re-fetch the entire list of domains every 30 seconds
  # or use junction?


  def __init__(self, *args, **kwargs):
    super(Crawler, self).__init__(*args, **kwargs)
    # TODO get domains from existing crawlers
    self.parent.request_domains(self)
    self.crawl()


  def crawl():
    greenhouse.map(
      lambda d: d.fetch_queued_pages(),
      self.domains(),
      pool_size=self.GREENLET_POOL_SIZE
    )

  @classmethod
  def resume_or_create(cls):
    ''' Entry-point for a new crawl process. '''
    for c in www.crawlers():
      if c.value + TIMEOUT < time.time():
        crawler = c
        'resuming crawler', c._dh['guid']
        c.crawl()
        return crawler
    'creating new crawler'
    return cls(parent=www)
