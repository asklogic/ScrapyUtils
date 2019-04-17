from base.components.prepare import Prepare

from .action import *
from .parse import *


class TestMockSinglePrepare(Prepare):
    _active = True
    SchemeList = [
        TestMockSingleAction,
        TestMockSingleParse,
    ]
    
    # ProcessorList = []

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"
        
        yield task
