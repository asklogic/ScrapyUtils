from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class TestMockFailedPrepare(Prepare):
    _active = True
    SchemeList = [
        TestMockFailedAction,
        TestMockFailedParse,
    ]
    
    # ProcessorList = []

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"
        
        yield task

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        raise Exception('test mock exception')

