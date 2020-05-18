from abc import abstractmethod
from queue import Queue
from typing import List, Callable

from base.components import StepSuit, Pipeline
from base.libs import Producer



class Command(object):
    exitcode: int = 0
    interrupt: bool = False

    do_collect: bool = True

    # def __init__(self):
    #     self.exitcode: int = 0
    #     self.interrupt: bool = False
    #     self.do_collect = True

    @classmethod
    def syntax(cls):
        return '[Thread]'

    @classmethod
    def command_config(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def command_components(cls, steps, processors, **kwargs):
        return steps, processors

    @classmethod
    def command_scraper(cls, **kwargs) -> None or Callable:
        return None

    @classmethod
    def command_task(cls, **kwargs) -> None or Callable:
        return None

    @classmethod
    @abstractmethod
    def run(cls, kw):
        pass

    @classmethod
    @abstractmethod
    def failed(cls):
        pass

    @classmethod
    @abstractmethod
    def signal_callback(cls, signum, frame):
        pass

    @classmethod
    @abstractmethod
    def exit(cls):
        pass


class ComponentMixin(object):
    config: dict = None
    tasks: Queue = None
    suits: List[StepSuit] = []
    pipeline: Pipeline = None
    proxy: Producer = None
