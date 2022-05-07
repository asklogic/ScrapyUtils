# -*- coding: utf-8 -*-
"""Processor.

Todo:
    * For module TODOs
    
"""
from abc import abstractmethod
from typing import Type, Optional, Union, List

from ScrapyUtils.components import Component, ComponentSuit
from ScrapyUtils.libs import Model


class Processor(Component):
    target: Type[Model] = Model

    @abstractmethod
    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        pass


class ProcessorSuit(ComponentSuit):
    target_components = Processor
    components: List[Processor] = []

    def process(self, model: Model):
        current = model

        for processor in self.components:

            if isinstance(current, processor.target):
                next_model = processor.process_item(current)

                # case 1: Return a modified model.
                if isinstance(next_model, processor.target):
                    current = next_model

                # case 2: Return false will interrupt loop.
                elif next_model is False:
                    break

                # case 3: Return None will continue.
                pass

        return True
