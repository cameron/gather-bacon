import re

from datahog.error import AliasInUse
import databacon as db
import greenhouse

from www import WWW



class Domain(db.Node):
  schema = str
  CRAWL_DELAY = 1
  domain = db.lookup.alias()
  crawl_queue = db.relation('Page')
  wwws = db.relation(WWW.domains)
#  pages = db.relation(Page.domain)
  num_pages = db.prop(int)


  def __init__(self, domain, *args, **kwargs):
    try:
      d = Domain.by_domain(domain)
    except AliasInUse as e:
      raise Exception("domain already exists! " + url)

    print 'creating domain'
    super(Domain, self).__init__(*args, **kwargs)
    print self._dh
    self.wwws.add(WWW.singleton())

  @property
  def www(self):
    print self.wwws._owner
    return list(self.wwws(limit=1))[0]


  def fetch_queued_pages(self, crawler):
    # TODO see what happens to the queue generator as pages are removed
    # hypothesis: it will skip whole pages due to the index shifts caused
    # by remove() that the generator isn't privy to
    print 'fetching queued pages', self.domain().value
    for page, rel in self.crawl_queue(nodes=True):
      page.fetch()
      self.crawl_queue.remove(page)
      crawler.heartbeat()
      greenhouse.scheduler.pause_for(self.CRAWL_DELAY)


  @classmethod
  def by_url(cls, url):
    domain_str = re.sub('\/.*', '', re.sub('https?:\/\/', '', url))
    print 'getting domain %s' % domain_str
    domain = cls.by_domain(url)
    if not domain:
      domain = cls(domain=domain_str)
    return domain

  # TODO
  # - guard against content farms / infinite web pages
