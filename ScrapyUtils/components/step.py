from abc import abstractmethod
from typing import *

from collections import deque
from ScrapyUtils.components.base import Component, ComponentMeta, ComponentSuit
from ScrapyUtils.libs import Scraper, Task, Model

from . import log


class StepMeta(ComponentMeta):
    """ """
    def __new__(mcs, name, bases, attrs: dict):
        return super().__new__(mcs, name, bases, attrs)

class Step(Component, metaclass=StepMeta):
    """ """
    # property
    # _context: dict
    # _scraper: Scraper
    # _models: List[Model]

    _suit = None

    def __init__(self, step_suit=None):
        self._suit: StepSuit = step_suit

    @property
    def context(self) -> dict:
        """ """

        return self._suit.context

    @property
    def scraper(self) -> Scraper:
        """ """

        return self._suit.scraper

    @property
    def content(self):
        """ """
        return self._suit.content

    @abstractmethod
    def check(self, content):
        """

        Args:
          content: 

        Returns:

        """
        pass

    @abstractmethod
    def do(self, task: Task):
        """

        Args:
          task: Task:
          task: Task:
          task: Task: 

        Returns:

        """

        pass


class ActionStep(Step):
    """ """
    priority = 600
    step_type = 'Action'

    @abstractmethod
    def scraping(self, task: Task):
        """

        Args:
          task: Task:
          task: Task:
          task: Task: 

        Returns:

        """

        pass

    @abstractmethod
    def check(self, content):
        """

        Args:
          content: 

        Returns:

        """
        pass

    def do(self, task: Task):
        """

        Args:
          task: Task:
          task: Task: 

        Returns:

        """

        try:
            content = self.scraping(task)
            if content:
                self.check(content)
                self._suit.content = content
            return True
        except Exception as e:
            # TODO: log out
            log.exception(e)
            # self.log.error('error', self.name)
            return False


class ParseStep(Step):
    """ """
    priority = 400
    step_type = 'Parse'

    @abstractmethod
    def parsing(self):
        """ """
        pass

    @abstractmethod
    def check(self, models: Deque[Model]):
        """

        Args:
          models: Deque[Model]: 

        Returns:

        """

        pass

    def do(self, task: Task):
        """

        Args:
          task: Task: 

        Returns:

        """


        try:
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
            log.exception(e)

            return False


class StepSuit(ComponentSuit):
    """ """
    # mounted
    target_components = Step

    _scraper: Scraper = None

    # def __init__(self, scraper: Scraper = None, steps: List[type(Step)] = None, config: dict = None):
    #     super(StepSuit, self).__init__(components=steps, config=config)
    #
    #     # assert scraper and isinstance(scraper, Scraper), 'StepSuit need a Scraper Instance.'
    #
    #     # suit property
    #     for step in self.steps:
    #         step._suit = self
    #
    #     self._scraper = scraper
    #
    #     # step property
    #     self.content: str = ''
    #     self.context: dict = {}
    #     self.models: Deque = deque()

    def __init__(self, *steps: List[Step] or Step):

        # single
        if type(steps) is list:
            for step in steps:
                assert issubclass(step, Step), 'StepSuit need Step type.'

        else:
            assert issubclass(steps, Step), 'StepSuit need Step type.'
            steps = List(steps)

        super(StepSuit, self).__init__(components=steps)

    def simple_task(self, url):
        """

        Args:
          url: 

        Returns:

        """
        task = Task(url=url)

        callback = self.closure_scrapy()

        callback(task)

    def suit_start(self):
        """ """
        super().suit_start()
        if not self.scraper.activated:
            self.scraper.scraper_activate()

    def suit_exit(self):
        """ """
        super().suit_exit()
        # if self.scraper.activated:
        self.scraper.scraper_quit()

    # def scrapy(self, task: Task):
    #     # TODO: abort
    #
    #     # self.models.clear()
    #     self.content = ''
    #
    #     for step in self.steps:
    #
    #         if not step.do(task):
    #             # error and log out
    #             logger.info('failed. count: {0}, url: {1}.'.format(task.count, task.url))
    #             return False
    #
    #     logger.info('success. url: {0}, models: {1}.'.format(task.url, len(self.models)))
    #     return True

    def closure_scrapy(self):
        """case success. return models. case failed. return task instance."""

        self.models.clear()
        self.content = ''

        def scrapy_inline(task: Task):
            """

            Args:
              task: Task:
              task: Task:
              task: Task:
              task: Task:
              task: Task:
              task: Task:
              task: Task:
              task: Task: 

            Returns:

            """

            for step in self.steps:

                if not step.do(task):
                    # error and log out
                    log.info('failed. count: {0}, url: {1}.'.format(task.count, task.url))
                    return False

            # log.info('success. url: {0}, param: {1}, models: {2}.'.format(task.url, str(task.param), len(self.models)))
            log.info('success. url: {0}, models: {2}.'.format(task.url, str(task.param), len(self.models)))
            return True

        return scrapy_inline

    @property
    def scraper(self) -> Scraper:
        """ """
        return self._scraper

    @property
    def steps(self) -> List[Step]:
        """ """
        return self._components


class BaseStepSuit(object):
    """ """
    steps: List = None
    content: str = None
    models: deque = None

    def __init__(self, *steps):
        self.steps = []
        self.content = ''
        self.models = deque()

        if len(steps) == 1 and type(steps[0]) == list:
            steps = steps[0]

        for step in steps:
            assert isinstance(step, type) and issubclass(step, BaseStep), 'StepSuit need Step type.'
            instance = step()
            instance.suit = self
            self.steps.append(instance)

    def simple_task(self, url):
        """

        Args:
          url: 

        Returns:

        """
        task = Task(url=url)

        for step in self.steps:
            step.do(task)


class BaseStep(object):
    """ """
    suit: BaseStepSuit = None

    @property
    def content(self):
        """ """
        return self.suit.content

    @abstractmethod
    def do(self, task: Task):
        """

        Args:
          task: Task:
          task: Task:
          task: Task:
          task: Task:
          task: Task:
          task: Task:
          task: Task:
          task: Task: 

        Returns:

        """
        pass


class BaseActionStep(BaseStep):
    """ """

    def do(self, task: Task):
        """

        Args:
          task(TaskModel): task instance.

        Returns:

        """

        # TODO: try - catch statement
        content = self.scraping(task)
        self.suit.content = content

    @abstractmethod
    def scraping(self, task):
        """

        Args:
          task(TaskModel): task instance.

        Returns:
          The content of pages.

        """
        pass


class BaseParseStep(BaseStep):
    """ """

    def do(self, task: Task):
        """

        Args:
          task: Task: 

        Returns:

        """

        models = deque()
        parsed = self.parsing()

        if parsed:
            for model in parsed:
                models.append(model)

        self.suit.models.extend(models)

    @abstractmethod
    def parsing(self):
        """ """
        pass

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
