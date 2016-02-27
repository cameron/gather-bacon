import greenhouse
import databacon as db
from www import WWW

class Page(db.Node):
  schema = unicode
  domain = db.relation('Domain')
  fetched = db.prop(int)
  url = db.lookup.alias()
  links = db.relation('Page')


  def __init__(self, url=None):
    # DH TODO adopt a pattern for passing kwargs to constructors
    # to create props
    super(Page, self).__init__()
    try:
      u = self.url(u)
    except AliasInUse as e:
      # TODO delete self
      print "page already exists! " + url
    # TODO steal domains from existing crawlers

  @property
  def domain(self):
    # TODO implement _attr prop caching? seems good for aliases
    return self._url.value[:self._url.value.indexOf('/')]

  def fetch(self):
    # TODO 2nd call for some kind of prop caching
    self.value = urllib2.urlopen(this.url().value)
    self.save()
    self.fetched(time.time())
    doc = html.fromstring(self.value)
    WWW.singleton().add_urls([href.attrs for href in doc.xpath('//a')])


  # TODO remove?
  # @classmethod
  # def by_urls(urls):
  #   pages = greenhouse.map(
  #     lambda u: Page.by_url(u) or Page(url=url),
  #     urls,
  #     pool_size=len(urls))
