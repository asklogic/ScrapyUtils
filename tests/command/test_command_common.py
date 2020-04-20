import unittest
from abc import abstractmethod
from typing import List

from queue import Queue

from base.libs import *
from base.components import *


class Command(object):
    exitcode: int = 0
    interrupt: bool = False

    do_collect: bool = True

    def __init__(self):
        self.exitcode: int = 0
        self.interrupt: bool = False
        self.do_collect = True

    @property
    def syntax(self):
        return '[Thread]'

    @classmethod
    @abstractmethod
    def signal_callback(self, signum, frame):
        pass

    @classmethod
    @abstractmethod
    def run(self):
        pass

    @classmethod
    @abstractmethod
    def failed(self):
        pass

    @classmethod
    @abstractmethod
    def exit(self):
        pass


class ComponentMixin(object):
    config: dict = None
    tasks: Queue = None
    suits: List[StepSuit] = None
    pipeline: Pipeline = None
    proxy: Producer = None


class TestCommandBase(unittest.TestCase):
    def test_demo(self):
        pass


if __name__ == '__main__':
    unittest.main()
