from typing import List
from unittest import TestCase
from unittest import SkipTest
import unittest
import warnings

from base.Prepare import Prepare

# mock prepare
from base.Scraper import Scraper, FireFoxScraper, RequestScraper
from base.task import Task

from base.Model import ModelManager, TaskModel


class MockNormalPrepare(Prepare):

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        f = FireFoxScraper(activated=False)
        return f

    @classmethod
    def task_prepared(cls) -> List[Task]:
        for i in range(10):
            t = Task()
            yield t


class MockDefaultPrepare(Prepare):
    pass


class MockFailedPrepare(Prepare):

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        return "some error str"

    @classmethod
    def task_prepared(cls) -> List[Task]:
        return 'another some error data'

class MockErrorPrepare(Prepare):

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        raise Exception('scraper prepared')

    @classmethod
    def task_prepared(cls) -> List[Task]:
        raise Exception('task prepared')


class TestPrepare(TestCase):

    def setUp(self) -> None:
        self.normal = MockNormalPrepare()
        self.failed = MockFailedPrepare()
        self.default = MockDefaultPrepare()
        self.error = MockErrorPrepare()

        ModelManager.add_model(TaskModel)
        super().setUp()

    # TODO
    @unittest.skip
    def test_start_prepare(self):
        self.fail()

    # TODO
    @unittest.skip
    def test_end_prepare(self):
        self.fail()

    # scraper prepared
    # should return a scraper instance
    # abstractmethod to overwrite
    def test_scraper_prepared(self):
        scraper = self.normal.scraper_prepared()

        self.assertIsInstance(scraper, FireFoxScraper)
        scraper.quit()

    def test_scraper_prepared_failed(self):
        scraper = self.failed.scraper_prepared()

        self.assertIsInstance(scraper, str)
        self.assertEqual('some error str', scraper)

        # exception in scraper_prepared
        with self.assertRaises(Exception) as e:
            self.error.scraper_prepared()

    def test_get_scraper(self):
        with self.assertWarns(UserWarning):
            scraper = self.default.get_scraper()
        self.assertIsInstance(scraper, RequestScraper)
        scraper.quit()

        scraper = self.normal.get_scraper()
        self.assertIsInstance(scraper, FireFoxScraper)
        scraper.quit()

    def test_get_scraper_failed(self):

        with self.assertWarns(UserWarning):
            failed_scraper = self.failed.get_scraper()

        self.assertIsInstance(failed_scraper, RequestScraper)
        failed_scraper.quit()

        with self.assertWarns(UserWarning):
            error_scraper = self.error.get_scraper()

        self.assertIsInstance(error_scraper, RequestScraper)
        error_scraper.quit()


    def test_get_scraper_thread_default(self):

        thread_number = 10

        with self.assertWarns(UserWarning):
            scrapers = [self.default.get_scraper() for x in range(thread_number)]

        for scraper in scrapers:
            self.assertIsInstance(scraper, RequestScraper)

        [x.quit() for x in scrapers]

    def test_get_scraper_thread_custom(self):

        thread_number = 4

        scrapers = [self.normal.get_scraper() for x in range(thread_number)]

        for scraper in scrapers:
            self.assertIsInstance(scraper, FireFoxScraper)
        [x.quit() for x in scrapers]

    def test_get_tasks(self):

        tasks = self.normal.get_tasks()

        for task in tasks:
           self.assertIsInstance(task, TaskModel)

    # return other instance
    def test_get_tasks_failed(self):
        with self.assertRaises(TypeError):
            tasks = self.failed.get_tasks()

    # no task return / yield
    def test_get_tasks_failed_empty(self):
        with self.assertRaises(Exception):
            tasks = self.default.get_tasks()


    # def test_generate_setting(self):
    #     self.fail()


