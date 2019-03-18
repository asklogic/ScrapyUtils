from abc import abstractmethod
from typing import Dict, Generator

from base.Model import Model
from base.Scraper import Scraper
from base.task import Task
from base.lib import ComponentMeta, Component


class SchemeMeta(ComponentMeta):
    # priority_index = 100

    def __new__(cls, name, bases, attrs: dict):
        # 在init里设置priority
        # if not attrs.get("priority") and name not in ["Action", "Parse"]:
        #     attrs["priority"] = cls.priority_index
        #     cls.priority_index = cls.priority_index + 100

        if not attrs.get("priority") and name not in ["Action", "Parse"]:
            attrs["priority"] = 0

        return super().__new__(cls, name, bases, attrs)


class Scheme(Component):
    _active: bool
    priority: int
    context: dict


class Action(Scheme, metaclass=SchemeMeta):
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


class Parse(Scheme, metaclass=SchemeMeta):
    def __init__(self):
        self.context: Dict = {}
        pass

    @abstractmethod
    def parsing(self, content: str) -> Model or Generator[Model]:
        pass
