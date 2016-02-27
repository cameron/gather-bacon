import databacon as db
import greenhouse
from www import WWW
from page import Page

class Domain(db.Node):
  CRAWL_DELAY = 1
  www = WWW
  domain = db.lookup.alias()
  crawl_queue = db.relation(Page)
  pages = db.relation(Page)
  num_pages = db.prop(int)


  def __init__(self, domain=None):
    # DB TODO: auto-generate a create-by-alias function that handles
    # node cleanup if the alias gets claimed before it can be associated
    # with the new node
    super(Page, self).__init__()
    try:
     d = self.domain(domain)
    except AliasInUse as e:
      # TODO delete self
      print "domain already exists! " + url


  def fetch_queued_pages(self):
    # TODO see what happens to the queue generator as pages are removed
    # hypothesis: it will skip whole pages due to the index shifts caused
    # by remove() that the generator isn't privy to
    for page, rel in self.crawl_queue(nodes=True):
      page.fetch()
      self.crawl_queue.remove(page)
      greenhouse.scheduler.pause_for(self.CRAWL_DELAY)
