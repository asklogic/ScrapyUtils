from base.components.step import ActionStep
from base.libs import Task


class First(ActionStep):
    priority = 700

    def scraping(self, task: Task):
        return self.scraper.get(task.url)


class Second(ActionStep):
    priority = 400


class Eno(ActionStep):
    priority = 600


class Third(ActionStep):
    priority = 300
