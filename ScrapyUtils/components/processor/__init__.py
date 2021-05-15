# -*- coding: utf-8 -*-
"""Processor module.

"""
from abc import abstractmethod
from typing import Optional, Union, Type

from ScrapyUtils.components import Component
from ScrapyUtils.libs import Model


class Processor(Component):
    target: Type[Model] = Model

    @abstractmethod
    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        """
        Args:
            model (Model): Process target.
        """
        pass

from .suit import ProcessorSuit