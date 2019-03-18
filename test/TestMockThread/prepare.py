from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class TestMockThreadPrepare(Prepare):
    _active = True
    schemeList = [
        TestMockThreadAction,
        TestMockThreadParse,
    ]

    Thread = 3
    Block = 2
    
    # processorList = []

    @classmethod
    def task_prepared(cls):
        for i in range(10):
            task = Task()
            task.url = "https://www.kuaidaili.com/free/inha/"
            task.param = i
            yield task
