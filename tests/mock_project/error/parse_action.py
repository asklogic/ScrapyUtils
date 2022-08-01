from typing import Iterator

from ScrapyUtils.components import active, Action
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.libs import Task, Scraper, Model
from ScrapyUtils.tool import XpathParser

from .model import ErrorModel


@active
class ErrorAction(Action):
    is_parser = True

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        parser = XpathParser(content.str_content)

        elements = parser.find_elements('/xpath_for_sequence_target')
        element = parser.find_element('/xpath_for_single_target')

        m = ErrorModel()
        m.field = "filed content"
        yield m

