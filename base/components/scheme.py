from abc import abstractmethod
from typing import Dict, Generator

from base.libs import Scraper, Task, Model, Field
# from base.libs.task import Task
# from base.libs.scraper import Scraper
from base.components.base import Component, ComponentMeta

from base.exception import HTTPStatusException


class SchemeMeta(ComponentMeta):

    def __new__(cls, name, bases, attrs: dict):
        # if not attrs.get("priority") and name not in ["Action", "Parse"]:
        #     attrs["priority"] = 0

        return super().__new__(cls, name, bases, attrs)


class Scheme(Component):
    _active: bool
    # priority: int
    context: dict

    # def scrapy_check(self):
    #     pass


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

    def scrapy_check(self, content: str, scraper: Scraper):
        status_code = scraper.get_status_code()

        if status_code > 400:
            raise HTTPStatusException()
        pass


class Parse(Scheme, metaclass=SchemeMeta):
    def __init__(self):
        self.context: Dict = {}
        pass

    @abstractmethod
    def parsing(self, content: str) -> Model or Generator[Model]:
        pass
