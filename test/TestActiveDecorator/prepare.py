from typing import List

from base.components import Prepare, active
from base.libs.task import Task
from base.libs.scraper import BaseScraper, RequestScraper, FireFoxScraper

from .action import *
from .parse import *
from .process import *


@active
class TestactivedecoratorPrepare(Prepare):
    # SchemeList = [
    #     TestactivedecoratorAction,
    #     TestactivedecoratorParse,
    # ]

    # ProcessorList = [
    #     TestactivedecoratorProcess,
    # ]

    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"

        yield task
