from base.components import Action, active
from base.libs.scraper import Scraper
from base.common import Task


@active
class TestsingleAction(Action):
    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)
