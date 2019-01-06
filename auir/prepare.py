# temp
from old.base.tools import firefoxScraper

from base.lib import Prepare, Task


class TestPrepare(Prepare):

    # @classmethod
    # def scraper_prepared(cls):
    #
    #     req = requestScraper
    #     return req

    @classmethod
    def task_prepared(cls):
        t = Task()
        t.url = "https://ip.cn"
        yield t


class IpProxyPrepare(Prepare):

    @classmethod
    def task_prepared(cls):
        t = Task()
        t.url = "https://www.kuaidaili.com/free/"
        yield t

class ScjstPrepare(Prepare):

    @classmethod
    def scraper_prepared(cls):
        f = firefoxScraper(headless=True)
        return f

    @classmethod
    def task_prepared(cls):
        t = Task()
        t.url = "http://xmgk.scjst.gov.cn/QueryInfo/Project/ProjectList.aspx"
        t.param = 3
        yield t