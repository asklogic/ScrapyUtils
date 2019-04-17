from base.components.scheme import Action
from base.libs.scraper import Scraper
from base.common import Task


class TestMockThreadAction(Action):
    _active = True

    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)


class TestPageAction(Action):
    _active = True

    def scraping(self, task: Task, scraper: Scraper) -> str:

        url = task.url +  str(task.param) + r'/'
        return scraper.get(url=url)