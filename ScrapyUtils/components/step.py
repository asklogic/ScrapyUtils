from abc import abstractmethod, ABC
from typing import *

from collections import deque
from ScrapyUtils.components.base import Component, ComponentSuit
from ScrapyUtils.libs import Scraper, Task


class BaseStep(object):
    """
    Note:
        To class Step.
    """

    @abstractmethod
    def do(self, task: Task):
        """Override method by ActionStep and ParseStep.


        Args:
             task (Task): The task that need to be executed in suit.

        """
        pass


class Step(Component, BaseStep):
    """The node of a StepSuit.

    Split the crawling/scraping action.

    Include two specified sub-class: ActionStep and BaseStep.

    Attributes:
        suit (str): The common suit instance.
        context (dict): The common context of suit.
    """

    suit = None

    def set_suit(self, suit):
        self.suit = suit

    @property
    def context(self):
        return self.suit.context


class BaseStepSuit(object):
    """A collection of steps and execute a singe mission(as task model).

    Just for a simple_task.

    The __init__ will be override in StepSuit.

    """
    steps: List = None
    models: deque = None

    def __init__(self, *steps):
        """Initialed step classes.

        Args:
            *steps:
        """
        self.steps = []
        self.models = deque()

        if len(steps) == 1 and type(steps[0]) == list:
            steps = steps[0]

        for step in steps:
            assert isinstance(step, type) and issubclass(step, BaseStep), 'StepSuit need Step type.'
            instance = step()
            self.steps.append(instance)

    def simple_task(self, url: str, scraper: Scraper = None):
        """Execute task model without initial and other modules.

        The url will be wrapped as a task instance.

        Args:
            url (str): String of url.
            scraper (Scraper): Scraper or not.

        """
        task = Task(url=url)

        content = ''

        for step in self.steps:
            if isinstance(step, ActionStep) or isinstance(step, BaseActionStep):
                content = step.scraping(task, scraper)
            elif isinstance(step, ParseStep) or isinstance(step, BaseParseStep):
                parsed = step.parsing(content)
                if parsed:
                    for model in parsed:
                        self.models.append(model)


class StepSuit(ComponentSuit, BaseStepSuit):
    """A component suit of steps.

    Collect the action and step component instance and run a task mission.

    Attributes:
        scraper (Scraper): The common scraper of suit.
        context (dict): The common context of suit.
        steps (list(steps)): The step instances.

    """
    target_components = Step

    scraper: Scraper = None
    context: dict = None
    models: deque = None

    def __init__(self, steps: List[type(Step)], config: dict = None):
        """
        Args:
            steps ():
            config ():
        """
        super(StepSuit, self).__init__(steps)

        for step in self.components:
            step.set_suit(self)

        self.context = dict()
        self.models = deque()

    def set_scraper(self, scraper: Scraper):
        """Set the scraper of suit.

        Methods will activated scraper.

        Args:
            scraper (Scraper): Scraper instance.
        """
        self.scraper = scraper
        if not self.scraper.activated:
            self.scraper.scraper_activate()

    def closure_scrapy(self):
        """Generate a callable that cloud be executed in ThreadPoolExecutor.

        The ThreadPoolExecutor will have timeout and raise any exception when step execute .


        Returns:
            scrapy_inline (function): The callable to execute the task.

        """

        self.models.clear()

        def scrapy_inline(task: Task):
            content = ''

            for step in self.steps:
                if isinstance(step, ActionStep):
                    current_content = step.scraping(task, self.scraper)
                    if current_content:
                        content = current_content
                elif isinstance(step, ParseStep):
                    parsed = step.parsing(content)
                    if parsed:
                        for model in parsed:
                            self.models.append(model)

            return True

        return scrapy_inline

    @property
    def steps(self):
        return self._components


class BaseActionStep(BaseStep):
    """Basic action steps that can work alone.

    Put the code of HTTP and other web action in the scraping method.

    Note:
        Extend the ActionStep instead of BaseActionStep.
    """

    @abstractmethod
    def scraping(self, task, scraper):
        """The overriding method should return the result of a web page.

        Args:
            scraper (Scraper): The Scraper instance of suit.
            task (TaskModel): A task instance.

        Returns:
            The content of pages.
        """
        pass


class ActionStep(Step, BaseActionStep):
    """The node of action.

    Put the code of HTTP and other web action in the scraping method.

    Attributes:
        priority (int): The priority step.
        scraper (Scraper): The common scraper of suit.

    """
    priority = 600

    # def do(self, task: Task):
    #     """The common method in StepSuit.
    #
    #     Note:
    #         Do not override it!
    #
    #     Args:
    #         task (TaskModel): Task instance.
    #
    #     """
    #     content = self.scraping(task, self.scraper)
    #     # TODO: check method.
    #     return content


class BaseParseStep(BaseStep):
    """Basic action steps that can work alone.

    Put the code of parsing in the parsing method.

    Note:
        Extend the ParseStep instead of BaseParseStep.
    """

    @abstractmethod
    def parsing(self, content):
        """The overriding method should pared the web page and should return the result.

        Args:
            content : The content of the web page.

        Returns:
            The result of parsing.
        """
        pass


class ParseStep(Step, BaseParseStep):
    """The Step parse the web page and yield the models.

    Note:
        Yield or return a iterable.

    Attributes:
        priority (int): The priority step.
        scraper (Scraper): The common scraper of suit.

    """
    priority = 400
