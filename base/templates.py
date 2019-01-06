#


# action

action_template = """from base.Action import Action
from base.Scraper import Scraper
from base.lib import Task


class $ActionClassName(Action):
    name = "$ActionName"

    @classmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: type) -> str:
        return scraper.get(url=task.url)
"""


# parse

parse_template = """from base.lib import Parse, ModelManager

from base.tools import xpathParse


class {0}Parse(Parse):
    def parsing(self, content: str, manager: ModelManager):
        pass

"""

# model

model_template = """from base.lib import Model


class {0}Model(Model):
    pass

"""

# conserve

conserve_template = """from base.lib import Conserve, allow, Model


class AgentConserve(Conserve):
    @allow(Model)
    def feed_func(self, model: Model):
        pass
"""

# prepare

prepare_template = """from base.tools import baseScraper, firefoxScraper, requestScraper

from base.lib import Prepare, Task


class {0}Prepare(Prepare):
    
    @classmethod
    def task_prepared(cls):
        task = Task()
        
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
    'conserve': '{1}Conserve',
}}

"""
