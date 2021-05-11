# -*- coding: utf-8 -*-
"""Processor module.

"""
from abc import abstractmethod
from typing import Optional, Type

from ScrapyUtils.components import Component
from ScrapyUtils.libs import Model


class Processor(Component):
    target: Type[Model] = Model

    @abstractmethod
    def process_item(self, model: Model) -> Optional[Model, False]:
        """
        Args:
            model (Model): Process target.
        """
        pass
