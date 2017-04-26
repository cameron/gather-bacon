import greenhouse
from datahog.error import AliasInUse
import databacon as db
from www import WWW
from domain import Domain

class Page(db.Node):
  schema = unicode

  # TODO upgrade to the more recent version of datahog that doens't have entities
  parent = Domain

  domain = db.relation('Domain')
  fetched = db.prop(int)
  url = db.lookup.alias()
  links = db.relation('Page')


  def _create(self, url=None, **kwargs):
    self.url(url)
    self.domain.add(Domain.by_url(url))
    self.fetched(0)


  @property
  def domain_str(self):
    # TODO implement _attr prop caching? seems good for aliases
    return self.url.value[:self.url.value.indexOf('/')]


  def fetch(self):
    # TODO 2nd call for some kind of prop caching
    self.value = urllib2.urlopen(this.url().value)
    self.save()
    self.fetched(time.time())
    doc = html.fromstring(self.value)
    urls = [href.attrs for href in doc.xpath('//a')]
    WWW.singleton().add_urls(urls)


  # TODO remove?
  # @classmethod
  # def by_urls(urls):
  #   pages = greenhouse.map(
  #     lambda u: Page.by_url(u) or Page(url=url),
  #     urls,
  #     pool_size=len(urls))
