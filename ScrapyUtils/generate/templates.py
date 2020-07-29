#


# action

action_template = """from ScrapyUtils.components import ActionStep, active
from ScrapyUtils.libs import Scraper
from ScrapyUtils.common import Task


@active
class ${class_name}Action(ActionStep):
    def scraping(self, task: Task):
        scraper: Scraper = self.scraper
        return scraper.get(url=task.url)

    def check(self, content):
        pass
"""

# parse

parse_template = """from typing import Generator, List

from ScrapyUtils.components import ParseStep, active, set_active
from .model import *

from ScrapyUtils.common import HiddenInputParse
from ScrapyUtils.tool import xpathParse, xpathParseList, XpathParser


@active
class ${class_name}Parse(ParseStep):

    def parsing(self) -> Model or Generator[Model]:
        parser = XpathParser(self.content)
        
        m = ${class_name}Model()
        m.filed = "filed content"
        yield m

    def check(self, models: List[Model]):
        pass
"""

# model

model_template = """from ScrapyUtils.libs import Model, Field


class ${class_name}Model(Model):
    filed = Field()
"""

# process

process_template = """from typing import Any

from ScrapyUtils.components import Processor, active, set_active
from ScrapyUtils.common import DumpInPeeweeProcessor, DuplicateProcessor, JsonFileProcessor, CSVFileProcessor

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

# config

config_template = r"""
{0} = {{
    'name': '{0}',
    'allow': [
        '{1}Action',
        '{1}Parse',
    ],
    'prepare': '{1}Prepare',
    'process': '{1}Process',
}}

"""

# settings

settings_template = r'''# -*- coding: utf-8 -*-
"""
scheme's profile for atom scheme.

generate by Generate command.
"""

from ScrapyUtils.libs import Task

THREAD = 2
TIMEOUT = 2

PROXY = False
PROXY_URL = ''


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
# DOWNLOAD_FOLDER = join([sep, 'atom', 'download'])
# DOWNLOAD_PATH =

'''
