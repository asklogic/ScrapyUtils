from typing import Optional, Iterator

from ScrapyUtils.components import Action, set_active, active
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.libs import Task, Scraper, Model


@active
class TestAction(Action):

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        page_content = scraper.get(task.url)
        content.str_content = page_content
