from typing import List

from base.Prepare import Prepare

# temp
from base.Scraper import Scraper, RequestScraper
from base.lib import Task


class DefaultPrepare(Prepare):
    name = "default"

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        r.set_timeout(5)
        return r

    @classmethod
    def task_prepared(cls):
        t = Task()

        for i in range(1, 300):
            t = Task()
            t.url = "http://xmgk.scjst.gov.cn/QueryInfo/Project/ProjectList.aspx"
            t.param = i
            yield t

class UpworkPrepare(Prepare):

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        r.set_timeout(5)
        return r

    @classmethod
    def task_prepared(cls) -> List[Task]:
        t = Task()

        for i in range(1, 300):
            t = Task()
            t.url = "https://www.otodom.pl/oferta/loft-na-pradze-ID3RkjG.html#1382fb9d9d"
            yield t