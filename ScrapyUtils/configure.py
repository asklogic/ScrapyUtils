from typing import Callable, Dict, List, Type, Union, Iterator, Optional
from types import ModuleType

from os import path
from queue import Queue

from ScrapyUtils.components import Component, Step, StepSuit, Action, Parse, Processor, ProcessorSuit
from ScrapyUtils.libs import Scraper, Task

# preload
# ----------------------------------------------------------------------
# callable
tasks_callable: Optional[Iterator[Task]] = None
scraper_callable: Optional[Callable] = None

# components
action_classes: List[Type[Action]] = []
parse_classes: List[Type[Parse]] = []
processor_classes: List[Type[Step]] = []

# initial
# ----------------------------------------------------------------------

# instances
tasks: Queue = Queue()
scrapers: List[Scraper] = []

# suits
step_suits: Optional[List[StepSuit]] = None
processor_suit: Optional[ProcessorSuit] = None

# models_pipeline: Pipeline = None

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
