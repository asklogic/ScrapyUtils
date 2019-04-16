from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class TestMockThreadPrepare(Prepare):
    _active = True
    SchemeList = [
        # TestMockThreadAction,
        'TestPageAction',
        # TestMockThreadParse,
        Mapping,
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
