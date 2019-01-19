from base.tools import baseScraper, requestScraper

from base.lib import Prepare, Task


class Generator_testPrepare(Prepare):
    
    @classmethod
    def task_prepared(cls):
        task = Task()
        task.urk = "about:blank"
        
        yield task
