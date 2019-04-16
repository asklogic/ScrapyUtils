from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class TestMockCustomPrepare(Prepare):
    _active = True
    SchemeList = [
        TestMockCustomAction,
        'TestAction',
        TestMockCustomParse,
    ]

    Block = 0.4

    ProxyURL = 'https://docs.python.org/3/library/urllib.request.html#module-urllib.request'


    
    # ProcessorList = []

    @classmethod
    def task_prepared(cls):

        for i in range(10):
            task = Task()
            task.url = 'https://www.kuaidaili.com/free/inha/'
            task.param = i
            yield task

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        return r


