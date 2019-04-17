from base.components.prepare import Prepare

from .action import *
from .parse import *


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

