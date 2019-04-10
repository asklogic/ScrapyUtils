from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class TestMockErrorPrepare(Prepare):
    _active = True
    schemeList = [
        TestMockErrorAction,
        TestMockErrorParse,
    ]
    
    # processorList = []

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"
        raise Exception('error')
        yield task

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        raise Exception('error')


