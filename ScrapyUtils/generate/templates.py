# action

action_template = """from typing import Optional, Iterator

from ScrapyUtils.components import Action, active
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.libs import Task, Scraper, Model

from ScrapyUtils.libs.scraper.request_scraper import RequestScraper
from ScrapyUtils.libs.scraper.firefox_scraper import FireFoxScraper


@active
class ${class_name}Action(Action):

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        page_content = scraper.get(task.url)
        content.str_content = page_content

"""

# model

model_template = """from ScrapyUtils.libs import Model, Field


class ${class_name}Model(Model):
    field = Field()
"""

# process

process_template = """from typing import Any

from ScrapyUtils.components import Processor, active, set_active
from ScrapyUtils.common import JsonFileProcessor, CSVFileProcessor, ExeclFileProcessor

from .model import *


@active
class ${class_name}Process(Processor):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data)
        return model        
"""

# prepare

prepare_template = """from typing import List

from ScrapyUtils.components import Prepare, active
from ScrapyUtils.libs.task import Task
from ScrapyUtils.libs.scraper import BaseScraper, RequestScraper, FireFoxScraper

from .action import *
from .parse import *
from .process import *

@active
class ${class_name}Prepare(Prepare):
    # SchemeList = [
    #     ${class_name}Action,
    #     ${class_name}Parse,
    # ]
    
    # ProcessorList = [
    #     ${class_name}Process,
    # ]
    
    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "about:blank"
        
        yield task
"""

# settings

settings_template = r'''# -*- coding: utf-8 -*-
"""
Setting for ${class_name} scheme.

generate by Generate command.
"""

from ScrapyUtils.libs import Task

THREAD: int = 2
"""The thread number"""
DELAY = 2
"""The delay for every task."""
RETRY: int = 3
"""The retry times."""
TIMEOUT: int = 15
"""The limit of a single task execute time."""


# generator your tasks in here.

def generate_tasks(**kwargs):
    for i in range(10):
        t = Task(url='http://yoursite.com')
        yield t


# setting your scraper here.
# default scraper is RequestScraper.
def generate_scraper(**kwargs):
    pass

# from os.path import join, sep

# DOWNLOAD_SUFFIX = 'html'
# DOWNLOAD_FOLDER = join('{class_name}', 'download')
# DOWNLOAD_PATH =

'''

init_template = """from ScrapyUtils.core.preload import collect_action, collect_processors, initial_configure

from . import action, processor, settings

steps_class = collect_action(action)
processors_class = collect_processors(processor)
initial_configure(settings)
"""
