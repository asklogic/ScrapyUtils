# -*- coding: utf-8 -*-
"""StepSuit module.

执行一系列Step动作的的最小单元。

"""
from typing import Union, Type, Optional, List, Sequence, Tuple
from collections import deque

from ScrapyUtils.libs import Task, Scraper, Model

from ..component import ComponentSuit, Component
from . import Step, Action, Parse


class StepSuit(ComponentSuit):
    """SuitSuit class for execute a task.

    StepSuit用于集中管理一系列的Step的启停和执行顺序，同时通过这些Step来执行一次流程。

    StepSuit通过传入一个Task对象来执行一次流程。
    """
    target_components = Step

    context: dict = None
    """dict: 共享字典用于同一个Suit下Steps之间的数据交换"""

    step_result_list: List[Tuple[int, Step, Union[str, Sequence[Model]]]] = None

    scraper: Scraper = None
    """Scraper: StepSuit的爬取类"""

    def __init__(self, components: Sequence[Component] = None):
        self.context = dict()
        self.step_result_list = list()

        super().__init__(components)

    def add_component(self, component: Step) -> Optional[Step]:
        """Override from Component.add_component

        添加前需要将Suit的共用context赋给Step

        Args:
            component (Step): Step类

        Returns:
            Optional[Component]: 如果成功添加，则返回Step类本身；否则返回None。
        """
        if success_component := super().add_component(component):
            success_component.__context = self.context
            return success_component

    def set_scraper(self, scraper: Scraper) -> Scraper:
        """Set a scraper.

        如果Scraper类没有正常开启，则会自动调用scraper_attach

        Args:
            scraper (Scraper): Suit的scraper类。

        Returns:
            Scraper: Scraper类本身。
        """
        assert isinstance(scraper, Scraper), 'Need Scraper instance.'

        self.scraper = scraper

        if not scraper.attached:
            scraper.scraper_attach()
        return self.scraper

    # def generate_scrapy_callable(self) -> Callable[[Task], bool]:
    #     return lambda task: do_scrapy(self, task)

    def do_scrape(self, task: Task):

        assert isinstance(task, Task), 'Do scrape need a task instance.'
        self.step_result_list.clear()

        for index, step in enumerate(self.components):
            # case: action
            if isinstance(step, Action):
                action_result = step.scraping(task=task, scraper=self.scraper)
                self.step_result_list.append((index, step, action_result))

            # case
            elif isinstance(step, Parse):
                # find last action_result
                current_content = ''
                for i in range(len(self.step_result_list) - 1, -1, -1):
                    if isinstance(self.step_result_list[i][1], Action) and not self.step_result_list[i][2]:
                        current_content = self.step_result_list[i][2]

                parse_result = step.parsing(content=current_content)
                self.step_result_list.append((index, step, parse_result))

# def do_scrapy(suit: StepSuit, task: Task) -> bool:
#     current_content = ''
#
#     for step in suit.components:
#         # case: action
#         if isinstance(step, Action):
#             current_content = step.scraping(task, suit.scraper)
#             if current_content:
#                 current_content = current_content
#         # case: parse
#         elif isinstance(step, Parse):
#             parsed = step.parsing(current_content)
#             if parsed:
#                 for model in parsed:
#                     suit.models.append(model)
#
#     return True
