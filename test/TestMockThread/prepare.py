from base.libs.scraper import RequestScraper
from base.components.prepare import Prepare

from .action import *
from .parse import *


class TestMockThreadPrepare(Prepare):
    _active = True
    SchemeList = [
        # TestMockThreadAction,
        'TestPageAction',
        # TestMockThreadParse,
    ]

    # ProcessorList = []

    Block = 1
    Thread = 3

    @classmethod
    def task_prepared(cls):
        for i in range(2,10):
            task = Task()
            task.url = 'https://www.kuaidaili.com/free/inha/'
            task.param = i
            yield task

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        r.set_timeout(5)
        return r
