import warnings
from abc import abstractmethod
from typing import List, Tuple

from base.components.base import Component, ComponentMeta
from base.libs.scraper import Scraper, RequestScraper
from base.libs.setting import BaseSetting, Setting
from base.libs.task import Task, TaskModel


class BasePrepare(Component, BaseSetting, metaclass=ComponentMeta):
    # component property
    _name: str
    _active: bool


class Prepare(BasePrepare, BaseSetting):
    Force: bool = True

    def __int__(self):
        self.start_prepare()

    def __del__(self):
        self.end_prepare()

    # TODO
    def start_prepare(self):
        pass

    # TODO
    def end_prepare(self):
        pass

    @classmethod
    @abstractmethod
    def scraper_prepared(cls) -> Scraper:
        pass

    @classmethod
    @abstractmethod
    def task_prepared(cls) -> List[Task]:
        """
        可以返回单个Task也可以返回一个Generator
        :return:
        """
        pass

    @classmethod
    def do(cls) -> Tuple[Scraper, List[Task]]:
        scraper = cls.scraper_prepared()
        tasks = cls.task_prepared()

        try:
            tasks = list(cls.task_prepared())
        except TypeError as te:
            raise TypeError("function task_prepared must return a iterable")
        return scraper, tasks

    @classmethod
    def get_scraper(cls) -> Scraper:
        try:
            scraper = cls.scraper_prepared()
            if isinstance(scraper, Scraper):
                return scraper
            else:
                warnings.warn('scraper_prepared must return a Scraper Instance. use default RequestScraper ')
                r = RequestScraper()
                r.set_timeout(5)
                return r

        # TODO
        except Exception as e:
            warnings.warn('failed in scraper_prepared. use default RequestScraper ')
            r = RequestScraper()
            r.set_timeout(5)
            return r

    @classmethod
    def get_tasks(cls) -> List[Task]:
        iterable = cls.task_prepared()

        if iterable is None:
            raise Exception("didn't yield task.")
        try:
            tasks = list(iterable)
        except TypeError as te:
            raise TypeError("task_prepared must return a iterable")

        for task in tasks:
            if not isinstance(task, TaskModel):
                raise TypeError("task_prepared must yield Task Instance")

        return tasks

    def generate(self):
        setting = Setting()