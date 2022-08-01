# -*- coding: utf-8 -*-
"""Process.

Todo:
    * For module TODOs
    
"""
from abc import abstractmethod
from typing import Type, Optional, Union, List

from ScrapyUtils.components import Component
from ScrapyUtils.libs import Model


class Process(Component):
    target: Type[Model] = Model

    next = None

    @abstractmethod
    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        pass

    def do_process_linked(self, model: Model):
        # current node process
        process_result = self.process_item(model)

        # case: if result is not False, continue next node.
        if process_result is not False and self.next:
            # if result is a modified model instance, process this model.
            self.next.do_process_linked(process_result if isinstance(process_result, Model) else model)

    def generate_callback(self, model: Model):
        return lambda: self.do_process_linked(model=model)
