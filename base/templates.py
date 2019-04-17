#


# action

action_template = """from base.components.scheme import Action
from base.libs.scraper import Scraper
from base.common import Task


class ${class_name}Action(Action):
    _active = True

    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)
"""

# parse

parse_template = """from typing import Generator

from base.components.model import ModelManager
from base.components.scheme import Parse
from .model import *

from base.common import DefaultXpathParse, HiddenInputParse
from base.tool import xpathParse, xpathParseList 


class ${class_name}Parse(Parse):
    _active = True

    def parsing(self, content: str) -> Model or Generator[Model]:
        m = ModelManager.model('${class_name}Model')
        m.filed = "filed content"
        yield m
"""

# model

model_template = """from base.components.model import Field, Model


class ${class_name}Model(Model):
    _active = True
    
    filed = Field()


"""

# process

process_template = """from typing import Any

from base.components.proceesor import Processor
from base.common import DumpInPeeweeProcessor, DuplicateProcessor, JsonFileProcessor


from .model import *


class ${class_name}Process(Processor):
    _active = True

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model        
"""

# prepare

prepare_template = """from typing import List

from base.components.prepare import Prepare
from base.libs.task import Task
from base.libs.scraper import BaseScraper,RequestScraper,FireFoxScraper


from .action import *
from .parse import *
from .process import *


class ${class_name}Prepare(Prepare):
    _active = True
    SchemeList = [
        ${class_name}Action,
        ${class_name}Parse,
    ]
    
    # ProcessorList = []

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
