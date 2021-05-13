# -*- coding: utf-8 -*-
"""StepSuit module.

Todo:
    * For module TODOs
    
"""
import random
from typing import Union, Type, Optional, List, Callable
from collections import deque

from ScrapyUtils.libs import Task, Scraper

from ..component import ComponentSuit, Component
from . import Step, Action, Parse


class StepSuit(ComponentSuit):
    # common
    components: List[Step] = []
    target_components = Step

    context: dict = None
    models: deque = None
    scraper: Scraper = None

    def __init__(self, components: List[Union[Type[Component], Component]] = []):
        self.context = dict()
        self.models = deque()
        super().__init__(components)

    def add_component(self, component: Union[Type[Step], Step]) -> Optional[Step]:
        # fixed super method
        step = ComponentSuit.add_component(self, component)

        if step:
            step.suit = self
            return step

    def set_scraper(self, scraper: Scraper) -> Scraper:
        assert isinstance(scraper, Scraper), 'Need Scraper instance.'

        self.scraper = scraper

        if not scraper.attached:
            scraper.scraper_attach()

        return self.scraper

    def generate_scrapy_callable(self) -> Callable[[Task], bool]:
        return lambda task: do_scrapy(self, task)


def do_scrapy(suit: StepSuit, task: Task) -> bool:
    current_content = ''

    for step in suit.components:
        # case: action
        if isinstance(step, Action):
            current_content = step.scraping(task, suit.scraper)
            if current_content:
                current_content = current_content
        # case: parse
        elif isinstance(step, Parse):
            parsed = step.parsing(current_content)
            if parsed:
                for model in parsed:
                    suit.models.append(model)

    return True

# from typing import Dict, Tuple, Literal
# import random
#
# names: List[str] = ['Ana', 'John', 'Lil']
#
# line_count: Dict[str, int] = {
#     'logger.py': 80,
#     'engine.py': 200,
#     'listener.py': 251,
# }
#
#
# def inner(contents: List[str]) -> bool:
#     return True
#
#
# inner: Callable[[List[str]], bool]
#
# point: Literal[int, int] = [314, 156]
#
#
# def ran() -> Union[int, str]:
#     return random.choice([134, 'message'])
StepSuit.__annotations__