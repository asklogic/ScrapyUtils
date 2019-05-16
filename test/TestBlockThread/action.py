from base.components import Action, active
from base.libs.scraper import Scraper
from base.common import Task


@active
class TestblockthreadAction(Action):

    def scraping(self, task: Task, scraper: Scraper) -> str:
        import time
        time.sleep(0.3)

        import random

        if random.choice([False, False, False, False, False, True]):
            raise Exception('random failed')
        return '<content>'
        # return scraper.get(url=task.url)
