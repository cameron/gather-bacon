import greenhouse
import databacon as db
from lib import profile
Page = Domain = None

class WWW(db.Node):
  NAME = 'the one and only'
  name = db.lookup.alias()
  domains = db.relation('Domain')
  num_domains = db.prop(int)
  num_pages = db.prop(int)
  crawlers = db.children('Crawler')
  lock_crawler_domains = db.lock()

  # ICK avoid circular deps
  @staticmethod
  def import_page_and_domain():
    global Page,  Domain
    from page import Page as p
    from domain import Domain as d
    Page = p
    Domain = d


  @classmethod
  def singleton(cls):
    cls.import_page_and_domain()

    www = WWW.by_name(cls.NAME)
    if not www:
      www = WWW()
      n = www.name()
      n.value = cls.NAME
      n.save()
      print 'domains', www.num_domains().value
      print 'pages', www.num_pages().value
      print 'getting crawlers'
      cs = list(www.crawlers())
      print 'crawlers', len(cs)
      print 'init singleton'

    return www


  def add_url(self, url):
    import pdb; pdb.set_trace()
    page = Page.by_url(url)
    if not page:
      page = Page(url=url)
      domain = Domain.by_domain(page.domain)
      if not domain:
        domain = Domain(domain=page.domain, parent=self)
      # TODO these could be parallelized
      domain.pages.add(page)
      domain.num_pages.increment()
      self.num_pages.increment()
      domain.queue.add(page)
    return page


  def add_urls(self, urls):
    done = profile('add urls')
    pages = greenhouse.map(
      lambda url: self.add_url(url),
      pages,
      pool_size=len(pages)
    )
    done()


  # TODO see about a nice pattern for overiding
  # `inst.collection.add`
  def add_crawler(self, new_crawler):
    # TODO consider recovery case when a process
    # dies holding the lock
    # - write a file to disk that can be read on restart
    #   to indicate that a lock should be released?
    print 'request domains'
    with self.lock_crawler_domains(interval=1, max_attempts=100):
      print 'getting list of crawlers'
      crawlers = list(self.crawlers())
      new_total_crawlers = len(crawlers) + 1
      print 'got crawlers'
      for crawler in crawlers:
        print 'crawler', c
        for idx, domain in enumerate(crawler.domains()):
          if idx % new_total_crawlers == 0:
            print 'reassigning', domain,
            crawler.domains.remove(domain)
            new_crawler.domains.add(domain)
      print 'done shuffling domains'

    # TODO
    # - monitor crawler activity and sleep crawler if
    #   heartbeat is > 30 seconds old
    # - page rank!

    # ANOTHER
    # implement rewind, tagging, and testing on top of the postgres opcode log
