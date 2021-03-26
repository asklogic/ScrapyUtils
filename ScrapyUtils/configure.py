from typing import Callable, Dict, List, Type
from types import ModuleType

from os import path
from queue import Queue

from ScrapyUtils.components import Component, Step, StepSuit, ActionStep, ParseStep, Processor, Pipeline, ProcessorSuit
from ScrapyUtils.libs import Scraper, RequestScraper, Proxy, MultiProducer, Producer

# preload
# ----------------------------------------------------------------------
# callable
tasks_callable: Callable = None
scraper_callable: Callable = None

# components
processors_class: List[Type[Step]] = None
steps_class: List[Type[Step]] = None

# initial
# ----------------------------------------------------------------------

# instances
tasks: Queue = Queue()
scrapers: List[Scraper] = None

# suits
step_suits: List[StepSuit] = None
processor_suit: ProcessorSuit = None

models_pipeline: Pipeline = None

# other
proxy: Producer = None

# settings variable
# ----------------------------------------------------------------------
SCHEME_PATH = path.sep

registered_keys = [
    'KEEP_LOG',
    'THREAD', 'TIMEOUT',

    # global
    'GLOBAL_KEY',
    'GLOBAL_TASK',
    'GLOBAL_SCRAPER',

    # data & file
    'DATA_FOLDER_PATH',

    # download
    'DOWNLOAD_FOLDER_PATH',
    'DOWNLOAD_SUFFIX',
    'DOWNLOAD_PATH',
]

KEEP_LOG = True

THREAD = 5
TIMEOUT = 1.5

# global
GLOBAL_KEY = False
GLOBAL_TASK = False
GLOBAL_SCRAPER = False

# data & file
DATA_FOLDER_PATH = path.join('data')

# download
DOWNLOAD_FOLDER_PATH = 'download'
DOWNLOAD_SUFFIX = '.html'
DOWNLOAD_PATH = None

if __name__ == '__main__':
    globals()['test'] = 'test'
    print(locals())
    print(globals())

    pass
