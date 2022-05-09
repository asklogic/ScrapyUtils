# -*- coding: utf-8 -*-
"""Example Google style docstrings.

"""
from abc import abstractmethod
from collections import deque
from functools import partial
from typing import List, Sequence, Any, Iterator, Optional, Union, NoReturn, Type, Callable

from ScrapyUtils.components import Component, ComponentSuit
from ScrapyUtils.libs import Task, Scraper, Model, Field
from ScrapyUtils.libs.scraper.request_scraper import RequestScraper


class ActionContent(Model):
    """
    In a single Task process, only one content object be created.
    """
    str_content: str = Field()
    bytes_content: bytes = Field()
    parameters: Any = Field(default_factory=dict)


class Action(Component):
    """
    The action in a task scraping.

    Different Actions means different actual action in web scraping.
    """
    is_parser: bool = False

    @abstractmethod
    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        """
        Extend this method to execute different action in single task scraping.

        Args:
            task (Task): The task instance that has URL and other infos.
            scraper (Scraper): The scraper to do actual HTTP action.
            content (ActionContent): The content in a single Task process.

        Returns:
            Iterator[Model]: The Infomation that need to be scraped will be wrapped as model and yield.
        """
        pass


class ActionSuit(ComponentSuit):
    """
    The action suit for execute a task mission.

    Each threads have one ActionSuit and it's Scraper.
    
    Scraper need to be set by method: set_scraper and Scraper will be activated automatically.
    """
    components: Sequence[Action]
    _scraper: Scraper = None

    def __init__(self, *components: Union[Type[Component], Component]):
        super().__init__(*components)

    @property
    def scraper(self) -> Scraper:
        if not self._scraper:
            self._scraper = RequestScraper()
        if not self._scraper.attached:
            return self._scraper.scraper_attach()
        return self._scraper

    def set_scraper(self, scraper: Scraper) -> Scraper:
        self._scraper = scraper
        return self._scraper

    def __do_scrape(self, task: Task) -> Sequence[Model]:
        action_content = ActionContent()

        parsed_model = deque()
        for action in self.components:
            # gathering
            if model_generator := action.action_step(task=task, scraper=self.scraper, content=action_content):
                for model in model_generator:
                    parsed_model.append(model)

        return parsed_model

    def generate_callback(self, task: Task) -> Callable[[], Sequence[Model]]:
        """
        Return a callback for the method can run without the suit object.

        Args:
            task (Task): Task instance.

        Returns:
            Callable[[], Sequence[Model]]: The callback
        """
        return partial(self.__do_scrape, task=task)
