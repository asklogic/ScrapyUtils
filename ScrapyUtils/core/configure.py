from typing import Callable, Dict, List
from types import ModuleType
from importlib import import_module

from . import collect
# from . import set_task_callable, set_scraper_callable

# temp
from os import path
from queue import Queue
from importlib import import_module
from urllib import parse
from concurrent.futures import ThreadPoolExecutor

from ScrapyUtils.components import Component, Step, StepSuit, ActionStep, ParseStep, Processor, Pipeline, ProcessorSuit
from ScrapyUtils.libs import Scraper, RequestScraper, Proxy, MultiProducer, Producer
from ScrapyUtils.log import common
from ScrapyUtils.log import basic

# global:
# *******************************************************************************

# components
processors_class: List[type(Step)] = None
steps_class: List[type(Step)] = None

# callable
tasks_callable: Callable = None
scraper_callable: Callable = None

config: dict = None

# ----------------------------------------------------------------------

tasks: Queue = Queue()
scrapers: List[Scraper] = None
proxy: Producer = None

# suits
step_suits: List[StepSuit] = None
processor_suit: ProcessorSuit = None

models_pipeline: Pipeline = None

# temp


# settings variable

KEEP_LOG = True

SCHEME_PATH = path.sep

THREAD = 5
TIMEOUT = 1.5

# FILE_FOLDER = None
# FILE_NAME = None

GLOBAL_KEY = False
GLOBAL_TASK = False
GLOBAL_SCRAPER = False

DOWNLOAD_FOLDER_PATH = 'download'
DOWNLOAD_SUFFIX = '.html'

DOWNLOAD_PATH = None

FILE_FOLDER_PATH = path.join('data')

# system

SCRAPER_TIMEOUT = 30

registered_keys = ['KEEP_LOG', 'THREAD', 'TIMEOUT', 'DOWNLOAD_FOLDER_PATH']


# callable

# task_callable: Callable = None
# scraper_callable: Callable = None


# feat


# feat

# def collect_scheme_preload(scheme: str):
#     module = import_module(scheme)
#
#     global steps_class, processors_class, tasks_callable, scraper_callable
#
#     steps_class = module.steps_class
#     processors_class = module.processors_class
#
#     # tasks_callable = module.tasks_callable
#     # scraper_callable = module.scraper_callable
#     #
#     # config = module.config


def initial_configure(settings_module: ModuleType):
    for key in registered_keys:
        if hasattr(settings_module, key):
            globals()[key] = getattr(settings_module, key)

    globals()['SCHEME_PATH'] = path.dirname(settings_module.__file__)

    # initial download configure items
    globals()['DOWNLOAD_FOLDER_PATH'] = path.join(path.dirname(settings_module.__file__), 'download')
    globals()['DOWNLOAD_SUFFIX'] = 'html'

    # tasks
    tasks_callable = getattr(settings_module, 'generate_tasks')
    assert callable(tasks_callable), "profile's generate_tasks must be callable."

    # scraper

    scraper_callable = getattr(settings_module, 'generate_scraper')
    assert callable(scraper_callable), "profile's generate_scraper must be callable."

    set_scraper_callable(scraper_callable)
    set_task_callable(tasks_callable)


# TODO: global configure
def collect_global_configure(settings_module: ModuleType):
    if GLOBAL_KEY:
        pass

    if GLOBAL_TASK:
        pass
    if GLOBAL_SCRAPER:
        pass

    settings = import_module('settings')


if __name__ == '__main__':
    globals()['test'] = 'test'
    print(locals())
    print(globals())

    pass
