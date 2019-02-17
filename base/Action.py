from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator

from base.Scraper import Scraper
from base.Model import ModelManager

# temp
from base.lib import Task,ComponentMeta


class Action(object, metaclass=ComponentMeta):
    def __init__(self):
        self.context: Dict = {}

    def delay(self):
        pass

    @abstractmethod
    def scraping(self, task: Task, scraper: Scraper) -> str:
        """
        进行http请求 获得网页内容
        :param task:
        :param scraper:
        :param manager:
        :return:
        """
        pass


class DefaultAction(Action):
    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)
