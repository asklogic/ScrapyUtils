from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator

from base.Scraper import Scraper
from base.Model import ModelManager

# temp
from base.lib import Task


class Action(object):

    def delay(self):
        pass

    @classmethod
    @abstractmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: ModelManager) -> str:
        """
        进行http请求 获得网页内容
        :param task:
        :param scraper:
        :param manager:
        :return:
        """
        pass


class DefaultAction(Action):
    @classmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: type) -> str:
        return scraper.get(url=task.url)
