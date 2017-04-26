import time 

import greenhouse

import databacon as db
from domain import Domain
from www import WWW
from lib import profile


class Crawler(db.Node):
  # number of page-fetching coroutines to run concurrently,
  # each one owning a domain
  CRAWLER_COROS = 50000

  # amount of time allowed to elapse without a heartbeat
  TIMEOUT = 30
  parent = WWW
  schema = int
  domains = db.relation(Domain)
  num_domains = db.prop(int)

  def __init__(self, *args, **kwargs):
    kwargs.setdefault('parent', WWW.singleton())
    super(Crawler, self).__init__(*args, **kwargs)
    if 'dh' not in kwargs:
      self.parent.add_crawler(self)


  def add_domain(domain):
    self.domains.add(domain)
    self.num_domains.increment()


  def crawl(self):
    domains = list(self.domains())
    print 'domains', domains
    print WWW.singleton().domains.of_type._meta
    # TODO handle no domains
    list(greenhouse.map(
      lambda d: d.fetch_queued_pages(),
      domains,
      pool_size=self.CRAWLER_COROS,
    ))


  def heartbeat(self):
    self.increment()


  @classmethod
  def wake_or_create(cls):
    ''' Entry-point for a new crawl process. '''
    print 'wake or create crawler...',
    for c in WWW.singleton().crawlers():
      if c.value + cls.TIMEOUT < time.time():
        crawler = c
        print 'awoke', c._dh['id']
        return crawler
    print 'creating'
    return cls()
