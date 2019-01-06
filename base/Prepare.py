from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator

from base.Scraper import Scraper, RequestScraper
# temp
from base.lib import Task


class BasePrepare(object):
    pass


class Prepare(BasePrepare):

    def __int__(self):
        self.start_prepare()

    def __del__(self):
        self.end_prepare()

    def start_prepare(self):
        pass

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
        scraper = cls.scraper_prepared()
        if isinstance(scraper, Scraper):
            # TODO
            return scraper
        raise Exception("scraper_prepared must return a Scraper Instance")

    @classmethod
    def get_tasks(cls) -> List[Task]:
        tasks = cls.task_prepared()
        try:
            tasks = list(cls.task_prepared())
        except TypeError as te:
            raise TypeError("function task_prepared must return a iterable")
        return tasks


# TODO
class DefaultRequestPrepare(Prepare):
    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        return r
