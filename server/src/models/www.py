import databacon as db
Page = Domain = None

class WWW(db.Entity):
  NAME = 'the one and only'
  name = db.lookup.alias()
  domains = db.relation('Domain')
  num_domains = db.prop(int)
  num_pages = db.prop(int)
  crawlers = db.relation('Crawler')
  request_domains_lock = db.prop(int)


  @classmethod
  def singleton(cls):
    global Page,  Domain
    from page import Page as p
    from domain import Domain as d
    Page = p
    Domain = d
    www =  WWW.by_name(cls.NAME)
    if not www:
      www = WWW()
      n = www.name()
      n.value = cls.NAME
      n.save()
      www.request_domains_lock(0)
    return www


  def add_url(self, url):
    page = Page.by_url(url)
    if not page:
      page = Page(url=url)
      domain = Domain.by_domain(page.domain)
      if not domain:
        domain = Domain(domain=page.domain, parent=self)
      # e.g., these could be parallelized
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


  def acquire_request_domains_lock(self):
    acquired = False
    while not acquired:
      lock = self.request_domains_lock
      try:
        lock.increment(limit=1)
        acquired = True
      except e:
        print e
        pass
      print 'www: acquire request domains lock failed, pausing 5'
      greenhouse.pause_for(5)


  def release_request_domains_lock(self):
    self.request_domains_lock(0)


  def request_domains(self, requester):
    self.acquire_request_domains_lock()
    crawlers = list(self.crawlers())
    new_total_crawlers = len(crawlers) + 1
    for crawler in crawlers():
      for idx, domain in enumerate(crawler.domains()):
        if idx % new_total_crawlers == 0:
          crawler.domains.remove(domain)
          requester.domains.add(domain)
    self.release_request_domains_lock()
