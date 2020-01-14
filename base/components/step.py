from abc import abstractmethod
from typing import *

from collections import deque
from base.components.base import Component, ComponentMeta
from base.libs import Scraper, Task, Model, ItemPool
from base.log import Wrapper as log
from base.log import current as logger


class StepMeta(ComponentMeta):
    def __new__(mcs, name, bases, attrs: dict):
        return super().__new__(mcs, name, bases, attrs)


class Step(Component, metaclass=StepMeta):
    # property
    # _context: dict
    # _scraper: Scraper
    # _models: List[Model]

    _suit = None

    def __init__(self, step_suit=None):
        self._suit: StepSuit = step_suit

    @property
    def context(self) -> dict:
        return self._suit.context

    @property
    def scraper(self) -> Scraper:
        return self._suit.scraper

    @property
    def content(self):
        return self._suit.content

    @abstractmethod
    def check(self, content):
        pass

    @abstractmethod
    def do(self, task: Task):
        pass


class ActionStep(Step):
    priority = 600

    @abstractmethod
    def scraping(self, task: Task):
        pass

    @abstractmethod
    def check(self, content):
        pass

    def do(self, task: Task):
        try:
            content = self.scraping(task)
            self.check(content)

            self._suit.content = content
            return True
        except Exception as e:
            # TODO: log out
            logger.exception(self.name, e)
            # self.log.error('error', self.name)
            return False


class ParseStep(Step):
    priority = 400

    @abstractmethod
    def parsing(self):
        pass

    @abstractmethod
    def check(self, models: Deque[Model]):
        pass

    def do(self, task: Task):
        try:
            # TODO: deque instead list
            models = deque()
            # FIXME: crit!

            parsed = self.parsing()
            if not parsed:
                return True
            for model in parsed:
                models.append(model)
            # models = list(self.parsing())
            self.check(models)

            self._suit.models.extend(models)
            return True

        except Exception as e:
            logger.exception(self.name, e)

            return False


class StepSuit(object):
    # mounted
    steps_class: List[type(Step)] = None

    _scraper: Scraper = None
    _steps: List[Step] = None

    def __init__(self, steps: List[type(Step)], scraper: Scraper, models: List[Model] = None):
        # assert
        for step in steps:
            assert isinstance(step, type), 'StepSuit need Step class.'
            assert issubclass(step, Step), 'StepSuit need Step class.'

        # assert scraper and callable(scraper), 'StepSuit need a callable.'
        assert scraper and isinstance(scraper, Scraper), 'StepSuit need a Scraper Instance.'

        # suit property
        self.steps_class = steps
        self._steps = None

        self._scraper = scraper

        # step property
        self.content: str = ''
        self.context: dict = {}
        self.models: Deque = models if models else deque()

    def suit_activate(self):
        self._steps = [x(self) for x in self.steps_class]

        # keep activated
        if not self.scraper.activated:
            self.scraper.scraper_activate()

    def suit_exit(self):
        # TODO: step exit
        self.scraper.scraper_quit()

    def scrapy(self, task: Task):

        self.models.clear()
        self.content = ''

        for step in self.steps:

            if not step.do(task):
                # error and log out
                logger.info('failed. count: {0}, url: {1}.'.format(task.count, task.url))
                return False

        logger.info('success. url: {0}, models: {1}.'.format(task.url, len(self.models)))
        return True

    def closure_scrapy(self):
        """
        case success. return models.
        case failed. return task instance.
        """

        self.models.clear()
        self.content = ''

        def scrapy_inline(task: Task):

            for step in self.steps:

                if not step.do(task):
                    # error and log out
                    logger.info('failed. count: {0}, url: {1}.'.format(task.count, task.url))
                    return False , task

            logger.info('success. url: {0}, models: {1}.'.format(task.url, len(self.models)))
            return True, task

        return scrapy_inline



    @property
    def scraper(self) -> Scraper:
        return self._scraper

    @property
    def steps(self) -> List[Step]:
        return self._steps

# class _StepSuit(object):
#     # property
#     steps: List[Step]
#
#     content: str = None
#     context: dict
#     models: List[Model]
#     scraper: Scraper
#     log: log
#
#     def __init__(self, steps: List[type(Step)], scraper: Scraper, pool: ItemPool = None, log=log, models=None):
#         # assert
#
#         for step in steps:
#             assert isinstance(step, type), 'StepSuit need Step class.'
#             assert issubclass(step, Step), 'StepSuit need Step class.'
#
#         assert scraper and isinstance(scraper, Scraper)
#
#         # step property
#         self.content = ''
#         self.context = {}
#         self.scraper = scraper
#         self.models = models if models else list()
#
#         # suit property
#         self._log = log
#         self._pool = pool
#
#         # init step objects
#         self.steps = [x(self) for x in steps]
#
#         # scraper active
#         # if not self.scraper.activated:
#         #     self.scraper.scraper_activate()
#
#         # pool
#         # if self.pool:
#         #     self.scraper.proxy = self.pool.get()
#
#     def scrapy(self, task: Task) -> bool:
#         """
#         :param task: current task
#         :return: current status. True means passed.
#         """
#         self.models.clear()
#         self.content = ''
#
#         for step in self.steps:
#             # TODO: refact
#             if not step.do(task):
#
#                 if self.pool:
#                     self.scraper.proxy = self.pool.get()
#
#                 self.log.info('failed. count: {0}, url: {1}.'.format(task.count, task.url))
#                 return False
#         self.log.info('success. url: {0}, models: {1}.'.format(task.url, len(self.models)))
#         return True
#
#     def closure_scrapy(self):
#
#         def inline():
#             return
#             pass
#
#     @property
#     def log(self):
#         return self._log
#
#     @property
#     def pool(self):
#         return self._pool
