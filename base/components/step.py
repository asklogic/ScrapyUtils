from abc import abstractmethod
from typing import *

from base.components.base import Component, ComponentMeta
from base.libs import Scraper, Task, Model
from base.log import logger


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

    @property
    def log(self):
        return self._suit.log

    @abstractmethod
    def check(self, content):
        pass

    def do(self, task: Task):
        if isinstance(self, ActionStep):
            try:
                content = self.scraping(task)
                self.check(content)

                self._suit.content = content
                return True
            except Exception as e:
                # TODO: log out
                self.log.exception(self.name, e)
                # self.log.error('error', self.name)
                return False
        elif isinstance(self, ParseStep):
            try:
                # TODO: deque instead list
                models = []
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
                self.log.exception(self.name, e)

                return False


class ActionStep(Step):
    priority = 600

    @abstractmethod
    def scraping(self, task: Task):
        pass

    @abstractmethod
    def check(self, content):
        pass


class ParseStep(Step):
    priority = 400

    @abstractmethod
    def parsing(self):
        pass

    @abstractmethod
    def check(self, models: List[Model]):
        pass


class StepSuit(object):
    # property
    steps: List[Step]

    content: str = None
    context: dict
    models: List[Model]
    scraper: Scraper
    log: logger

    def __init__(self, steps: List[type(Step)], scraper: Scraper, log=logger):
        # assert
        for step in steps:
            assert isinstance(step, type), 'StepSuit need Step class.'
            assert issubclass(step, Step), 'StepSuit need Step class.'

        assert scraper and isinstance(scraper, Scraper)

        # init property
        self.content = ''
        self.context = {}
        self.scraper = scraper
        self.models = []
        self.log = log

        # init step objects
        self.steps = [x(self) for x in steps]

        # scraper active
        assert scraper.activated is True, 'Scraper must be activated.'

    def scrapy(self, task: Task):
        self.models.clear()
        self.content = ''

        for step in self.steps:
            # TODO: refact
            if not step.do(task):
                self.log.info('failed. count: {0}, url: {1}.'.format(task.count, task.url))
                return
        self.log.info('success. url: {0}, models: {1}.'.format(task.url, len(self.models)))

    def log(self):
        pass
