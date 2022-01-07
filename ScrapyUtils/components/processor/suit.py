# -*- coding: utf-8 -*-
"""ProcessorSuit module.

"""
from typing import List

from ScrapyUtils.libs import Model

from ..component import Component, ComponentSuit
from . import Processor


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
