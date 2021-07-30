from ScrapyUtils.libs.scraper import Scraper
from .scraper.request_scraper import RequestScraper
from .scraper.firefox_scraper import FireFoxScraper, set_firefox_path, set_driver_path

from .model import Model, field, Task, Proxy

from .threads import BaseThread, Consumer, Producer

Field = field
