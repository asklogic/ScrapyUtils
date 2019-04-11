from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class TestMockPrepare(Prepare):
    _active = True
    SchemeList = [
        TestMockAction,
        TestMockParse,
    ]
    
    # processorList = []

    Block = 1

    @classmethod
    def task_prepared(cls):
        for i in range(10):
            task = Task()
            task.url = "https://www.kuaidaili.com/free/inha/"
            task.param = {
                'info' : 123,
            }
            yield task

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        r.set_timeout(10)
        return r
