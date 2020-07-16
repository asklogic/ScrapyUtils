from base.components.step import ActionStep
from base.components import active
from base.libs import Task


@active
class Actived(ActionStep):
    def scraping(self, task: Task):
        """
        Args:
            task (Task):
        """
        return self.scraper.get(task.url)


class Abort(ActionStep):
    pass
