from typing import List

from base.components import Prepare, active
from base.libs.task import Task
from base.libs.scraper import BaseScraper, RequestScraper, FireFoxScraper

from .action import *
from .parse import *
from .process import *


@active
class TestemptythreadPrepare(Prepare):
    # SchemeList = [
    #     TestemptythreadAction,
    #     TestemptythreadParse,
    # ]

    # ProcessorList = [
    #     TestemptythreadProcess,
    # ]

    @classmethod
    def task_prepared(cls):
        for i in range(50):
            task = Task()
            task.url = "about:blank"

            yield task

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        return r
