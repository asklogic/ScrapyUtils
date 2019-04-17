from base.components.prepare import Prepare

from .action import *
from .parse import *


class TestMockPrepare(Prepare):
    _active = True
    SchemeList = [
        TestMockAction,
        TestMockParse,
    ]

    Block = 1
    
    # ProcessorList = []

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"
        
        yield task
