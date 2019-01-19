#


# action

action_template = """from base.Action import Action
from base.Model import ModelManager
from base.Scraper import Scraper
from base.lib import Task


class ${class_name}Action(Action):
    @classmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: ModelManager) -> str:
        return scraper.get(url=task.url)
"""

# parse

parse_template = """from typing import Generator

from base.Model import ModelManager, Model
from base.Parse import Parse
from .model import *

from base.tool import xpathParse, xpathParseList


class ${class_name}Parse(Parse):
    def parsing(cls, content: str, manager: ModelManager) -> Model or Generator[Model]:
        pass
"""

# model

model_template = """from base.Model import Model, Field


class ${class_name}Model(Model):
    pass

"""

# process

process_template = """from typing import Any

from base.Model import Model
from base.Process import Process


class ${class_name}Process(Process):
    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
"""

# prepare

prepare_template = """from base.tools import baseScraper, requestScraper

from base.lib import Prepare, Task


class ${class_name}Prepare(Prepare):
    
    @classmethod
    def task_prepared(cls):
        task = Task()
        task.urk = "about:blank"
        
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
