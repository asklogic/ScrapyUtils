from typing import Optional, Iterator

from ScrapyUtils.components import Action, active
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.libs import Task, Scraper, Model

from ScrapyUtils.libs.scraper.request_scraper import RequestScraper
from ScrapyUtils.libs.scraper.firefox_scraper import FireFoxScraper


@active
class ErrorAction(Action):

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        page_content = scraper.get(task.url)
        content.str_content = page_content


assert False
