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
    str_content: str = Field()
    bytes_content: bytes = Field()
    handler: Any = Field()


class Action(Component):
    @abstractmethod
    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Optional[Iterator[Model]]:
        pass


class ActionSuit(ComponentSuit):
    components: Sequence[Action]
    _scraper: Scraper

    def __init__(self, *components: Union[Type[Component], Component]):
        super().__init__(*components)
        self._scraper = RequestScraper()

    @property
    def scraper(self):
        if not self._scraper:
            return self._scraper.scraper_attach()
        return self._scraper

    def set_scraper(self, scraper: Scraper) -> Scraper:
        self._scraper = scraper
        return self._scraper

    def __do_scrape(self, task: Task) -> Sequence[Model]:
        parsed_content = deque((ActionContent(),))

        parsed_model = deque()
        for action in self.components:
            # gathering
            if model_generator := action.action_step(task=task, scraper=self.scraper, content=parsed_content[-1]):
                for model in model_generator:
                    # to next action
                    if isinstance(model, ActionContent):
                        parsed_content.append(model)
                    # ...or yield a model
                    else:
                        parsed_model.append(model)

        return parsed_model

    def generate_callback(self, task: Task) -> Callable[[], Sequence[Model]]:
        return partial(self.__do_scrape, task=task)
