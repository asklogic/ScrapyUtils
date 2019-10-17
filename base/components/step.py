from abc import abstractmethod
from typing import *

from base.components.base import Component, ComponentMeta
from base.libs import Scraper, Task, Model


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

    def do(self, task: Task):
        if isinstance(self, ActionStep):
            try:
                content = self.scraping(task)
                self.check(content)

                self._suit.content = content
            except Exception as e:
                # TODO: log out
                pass
        elif isinstance(self, ParseStep):
            try:
                models = list(self.parsing())
                self.check(models)

                self._suit.models.extend(models)
            except Exception as e:
                pass


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

    def __init__(self, steps: List[type(Step)], scraper: Scraper):
        # assert
        assert isinstance(scraper, Scraper)
        for step in steps:
            assert issubclass(step, Step), 'Step class'

        # init step objects
        self.steps = [x(self) for x in steps]

        # init property
        self.content = ''
        self.context = {}
        self.scraper = scraper
        self.models = []

    def scrapy(self, task: Task):
        for step in self.steps:
            step.do(task)
