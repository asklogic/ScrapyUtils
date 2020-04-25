from base.components import ActionStep, active
from base.libs import Scraper
from base.common import Task


@active
class Test_preloadAction(ActionStep):
    def scraping(self, task: Task):
        scraper: Scraper = self.scraper
        return scraper.get(url=task.url)

    def check(self, content):
        pass
