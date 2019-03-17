from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class TestMockPrepare(Prepare):
    _active = True
    schemeList = [
        TestMockAction,
        TestMockParse,
    ]
    
    # processorList = []

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"
        
        yield task
