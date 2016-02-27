from lib import dev
import resources
resources.setup_dbpool()

from models.crawler import Crawler
Crawler.resume_or_create()
