from typing import Callable, Dict, List, Type, Union
from types import ModuleType

from os import path
from queue import Queue

from ScrapyUtils.components import Component, Step, StepSuit, ActionStep, ParseStep, Processor, Pipeline, ProcessorSuit
from ScrapyUtils.libs import Scraper, RequestScraper, FireFoxScraper

from ScrapyUtils.libs import Producer, Consumer

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
    # 日志
    'KEEP_LOG',

    # 线程数
    'THREAD',

    # 超时时间
    'TIMEOUT',

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

KEEP_LOG: bool = True

THREAD: int = 5
TIMEOUT: Union[int, float] = 1.5

# global
GLOBAL_KEY: bool = False
GLOBAL_TASK: bool = False
GLOBAL_SCRAPER: bool = False

# data & file
DATA_FOLDER_PATH: str = path.join('data')

# download
DOWNLOAD_FOLDER_PATH: str = 'download'
DOWNLOAD_SUFFIX: str = '.html'
DOWNLOAD_PATH: str = None
