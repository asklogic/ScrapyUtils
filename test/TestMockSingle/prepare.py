from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class TestMockSinglePrepare(Prepare):
    _active = True
    schemeList = [
        TestMockSingleAction,
        # TestMockSingleParse,
        Mapper
    ]

    # processorList = []

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "https://www.kuaidaili.com/free/inha/"
        task.param = 1
        yield task
