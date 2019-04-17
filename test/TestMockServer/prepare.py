from base.components.prepare import Prepare

from .action import *
from .parse import *


class TestMockServerPrepare(Prepare):
    _active = True
    SchemeList = [
        TestMockServerAction,
        TestMockServerParse,
    ]
    
    # ProcessorList = []

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"
        
        yield task
