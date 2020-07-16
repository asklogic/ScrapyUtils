from base.components.step import ActionStep
from base.components import active
from base.libs import Task


@active
class Single(ActionStep):
    # priority = 700

    def scraping(self, task: Task):
        """
        Args:
            task (Task):
        """
        return self.scraper.get(task.url)


class Abort(ActionStep):
    pass


@active
class Nooope(ActionStep):
    priority = 800
    pass
