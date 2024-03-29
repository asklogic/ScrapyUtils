from collections import deque
from typing import Callable, Dict, List, Type, Union, Iterator, Optional
from types import ModuleType

from os import path
from queue import Queue

from ScrapyUtils.components import Component, Action
from ScrapyUtils.components.process import Process
# from ScrapyUtils.core.pipeline import Pipeline
from ScrapyUtils.libs import Scraper, Task, Consumer

# preload
# ----------------------------------------------------------------------
project_package_path: str

# callable
tasks_callable: Callable[[], Iterator[Task]]
scraper_callable: Optional[Callable] = None

# component classes
action_classes: List[Type[Action]] = []
process_classes: List[Type[Process]] = list()

# initialed
# ----------------------------------------------------------------------

components: List[Component] = []

scrapers: List[Scraper] = []

# instances
tasks: Queue = Queue()
"""等待爬取的任务"""
failed_tasks: Queue = Queue()
"""爬取失败的任务"""
models: deque = deque()
"""等待处理的数据对象"""
failed_models = deque()
"""处理失败的数据对象"""

scrape_consumers: List[Consumer] = []
"""爬取线程列表"""
# models_pipeline: Pipeline
"""处理线程"""

# settings variable
# ----------------------------------------------------------------------
PROJECT_PATH = path.sep

registered_keys = [
    # 日志
    'KEEP_LOG',

    'THREAD',
    'DELAY',
    'TIMEOUT',
    'RETRY',

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
"""开启的线程数量"""
DELAY: Union[int, float] = 1.5
"""每一个爬取任务之间的时间间隔"""
TIMEOUT: int = 5
"""每一个爬取任务的最大完成时间，超出则认为该次爬取任务失败"""
RETRY: int = 3
"""每一个爬取任务的重试次数"""

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

# exit
EXIT_WAIT = 3
"""任务退出时等待时间"""
