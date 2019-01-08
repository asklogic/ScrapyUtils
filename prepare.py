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
        # t.url = "https://ip.cn/"
        # # t.url = "http://www.ip138.com/"
        # t.url = "https://www.kuaidaili.com/free/"
        # t.url = "http://xmgk.scjst.gov.cn/QueryInfo/Project/ProjectList.aspx"
        # t.param = 4
        # yield t

        for i in range(1, 300):
            t = Task()
            t.url = "http://xmgk.scjst.gov.cn/QueryInfo/Project/ProjectList.aspx"
            t.param = i
            yield t


class ProxyTestPrepare(Prepare):
    name = "test_prepare"

    @classmethod
    def task_prepared(cls) -> List[Task]:
        t = Task()
        t.url = "https://www.kuaidaili.com/free/"
        yield t
        pass


class ProxyTestThreadPrepare(Prepare):
    name = "test_thread_prepare"

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        r.set_timeout(5)
        return r

    @classmethod
    def task_prepared(cls) -> List[Task]:
        for i in range(1, 20):
            t = Task()
            t.url = "http://www.kuaidaili.com/free/inha/{0}/".format(i)
            yield t
