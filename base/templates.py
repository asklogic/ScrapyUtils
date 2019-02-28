#


# action

action_template = """from base.scheme import Action
from base.Scraper import Scraper
from base.common import Task


class ${class_name}Action(Action):
    _active = True

    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)
"""

# parse

parse_template = """from typing import Generator

from base.Model import ModelManager, Model
from base.scheme import Parse
from .model import *

from base.tool import xpathParse, xpathParseList
from base.common import DefaultXpathParse


class ${class_name}Parse(Parse):
    _active = True

    def parsing(self, content: str) -> Model or Generator[Model]:
        m = ModelManager.model('${class_name}Model')
        m.filed = "filed content"
        yield m
"""

# model

model_template = """from base.Model import Model, Field


class ${class_name}Model(Model):
    _active = True
    
    filed = Field()


"""

# process

process_template = """from typing import Any

from base.Model import Model
from base.Process import Processor
from base.common import JsonFileProcessor, DuplicateProcessor, DumpProcessor

from .model import *


class ${class_name}Process(Processor):
    _active = True

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model        
"""

# prepare

prepare_template = """from typing import List

from base.Scraper import BaseScraper, RequestScraper
from base.Prepare import Prepare
from base.task import Task

from .action import *
from .parse import *
from .process import *


class ${class_name}Prepare(Prepare):
    _active = True
    schemeList = [
        ${class_name}Action,
        ${class_name}Parse,
    ]
    
    # processorList = []

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
