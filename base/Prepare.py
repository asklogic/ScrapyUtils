from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import warnings

from base.Scraper import Scraper, RequestScraper

from base.lib import ComponentMeta, Component, Setting, BaseSetting
from base.scheme import Scheme
from base.Process import Processor
from base.task import Task
from base.Model import TaskModel


class BasePrepare(Component, BaseSetting, metaclass=ComponentMeta):
    # component property
    _name: str
    _active: bool

    # prepare property
    SchemeList: List[Scheme] = []
    ProcessorList: List[Processor] = []

    setting: Dict = {}

    # config
    ProxyAble: bool = False
    Thread: int = 5
    Block: int = 0.2


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
                warnings.warn('scraper_prepared must return a Scraper Instance. start default RequestScraper ')
                r = RequestScraper()
                r.set_timeout(5)
                return r

        # TODO
        except Exception as e:
            warnings.warn('failed in scraper_prepared. start default RequestScraper ')
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


# TODO
class DefaultRequestPrepare(Prepare):
    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        return r


# or ?
# FIXME
def get_default_scraper():
    r = RequestScraper()
    return r
