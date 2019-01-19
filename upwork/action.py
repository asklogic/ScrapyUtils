from base.Action import Action
from base.Model import ModelManager
from base.Scraper import Scraper
from base.lib import Task


class DetailAction(Action):
    @classmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: ModelManager) -> str:
        return scraper.get(url=task.url)
