# -*- coding: utf-8 -*-
"""Action module for component step.

"""
from abc import abstractmethod

from ScrapyUtils.libs import Task, Scraper
from . import Step


class Action(Step):
    priority: int = 600

    @abstractmethod
    def scraping(self, task: Task, scraper: Scraper) -> str:
        """The overriding method should return the result of a web page.

        Args:
            scraper (Scraper): The shared Scraper instance from suit.
            task (TaskModel): A task instance.

        Returns:
            str: The content of pages.
        """
        pass

    pass
