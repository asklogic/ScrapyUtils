from abc import abstractmethod
from typing import List
from queue import Queue

from base.libs import *
from base.components import *


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
    @abstractmethod
    def signal_callback(cls, signum, frame):
        pass

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
    def exit(cls):
        pass


class ComponentMixin(object):
    config: dict = None
    tasks: Queue = None
    suits: List[StepSuit] = None
    pipeline: Pipeline = None
    proxy: Producer = None
