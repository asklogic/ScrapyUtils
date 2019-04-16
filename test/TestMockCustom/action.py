from base.scheme import Action
from base.Scraper import Scraper
from base.common import Task


class TestMockCustomAction(Action):
    _active = True

    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)


class TestAction(Action):
    _active = True

    def scraping(self, task: Task, scraper: Scraper) -> str:
        pass
