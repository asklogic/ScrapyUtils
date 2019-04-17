from base.components.prepare import Prepare

from .action import *
from .parse import *


class TestMockErrorComPrepare(Prepare):
    _active = True
    SchemeList = [
        TestMockErrorComAction,
        'NotExistAction',
        TestMockErrorComParse,
    ]
    
    # ProcessorList = []

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"
        
        yield task
