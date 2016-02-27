
import greenhouse
urllib2 = greenhouse.patched("urllib2")

from app import app
from schema import User, URL, CrawlQueue
from route_utils import *
import http_exceptions as exceptions
import validate


cq = CrawlQueue

for page in cq():
  html = fetch(page.url().value)
  hrefs = links(html)
