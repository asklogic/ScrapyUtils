from ScrapyUtils.components import ActionStep, active
from ScrapyUtils.libs import Scraper
from ScrapyUtils.common import Task


@active
class AtomAction(ActionStep):
    def scraping(self, task: Task):
        scraper: Scraper = self.scraper
        return scraper.get(url=task.url)

    def check(self, content):
        pass
