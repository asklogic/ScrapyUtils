from unittest import TestCase

from base.Prepare import Prepare

# mock prepare
from base.Scraper import Scraper, FireFoxScraper


class MockNormalPrepare(Prepare):

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        f = FireFoxScraper(activated=False)
        return f


class MockFailedPrepare(Prepare):

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        return "some error str"


class TestPrepare(TestCase):

    def setUp(self) -> None:
        self.normal = MockNormalPrepare()
        self.failed = MockFailedPrepare()
        self.failed = MockFailedPrepare()
        super().setUp()

    # TODO
    def test_start_prepare(self):
        pass
        # self.fail()

    # TODO
    def test_end_prepare(self):
        pass
        # self.fail()

    # scraper prepared
    # should return a scraper instance
    # abstractmethod to overwrite
    def test_scraper_prepared(self):
        scraper = self.normal.scraper_prepared()

        self.assertIsInstance(scraper, FireFoxScraper)

    # get a scraper instance
    # def test_get_scraper(self):
    #     self.fail()
    #
    # def test_task_prepared(self):
    #     self.fail()
    #
    # def test_get_tasks(self):
    #     self.fail()
    #
    # def test_do(self):
    #     self.fail()
    #
    # def test_generate_setting(self):
    #     setting = MockNormalPrepare.generate()
    #     self.fail()
