from base.components.scheme import Action
from base.libs.scraper import Scraper
from base.common import Task


class TestMockServerAction(Action):
    _active = True

    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)
