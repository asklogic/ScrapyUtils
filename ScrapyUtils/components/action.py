# -*- coding: utf-8 -*-
"""Example Google style docstrings.

"""
from abc import abstractmethod
from typing import List, Any, Iterator, Callable

from ScrapyUtils.components import Component
from ScrapyUtils.libs import Task, Scraper, Model, Field


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
    """bool: The flag of parser. True == parser."""

    next = None
    """Action: Next action on the chain."""

    @abstractmethod
    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        """
        Extend this method to execute different action in single task scraping.

        Args:
            task (Task): The task instance that has URL and other infos.
            scraper (Scraper): The scraper to do actual HTTP action.
            content (ActionContent): The content in a single Task process.

        Yields:
            Model: Scraped Model.
        """
        pass

    def do_action_linked(self, task: Task, scraper: Scraper, content: ActionContent = None) -> Iterator[Model]:
        """Execute all action_step() in chain. 

        Args:
            task (Task): Scrape Task.
            scraper (Scraper): Scraper for HTTP.
            content (ActionContent, optional): The content in task processing. Defaults to None.

        Yields:
            Model: Scraped Model.
        """
        # create new content.
        content = content if content else ActionContent()

        # current linked node.
        if generator := self.action_step(task, scraper, content):
            yield from generator

        # next linked node.
        if self.next:
            yield from self.next.do_action_linked(task, scraper, content)

    def generate_callback(self, task: Task, scraper: Scraper) -> Callable[[], List[Model]]:
        """Generate a callback for pool.

        Args:
            task (Task): Scrape task.
            scraper (Scraper): Scraper for HTTP.

        Returns:
            Callable[[Task, Scraper], List[Model]]: The Scraped models from one single scrape task processing.
        """
        return lambda: list(self.do_action_linked(task, scraper))
