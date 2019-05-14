from base.components import Action, active
from base.libs.scraper import Scraper
from base.common import Task


@active
class TestemptythreadAction(Action):

    def scraping(self, task: Task, scraper: Scraper) -> str:
        # print('id ', id(scraper))
        import time
        time.sleep(0.3)
        return 'content'
