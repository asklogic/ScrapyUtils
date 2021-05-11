# -*- coding: utf-8 -*-
"""Example Google style docstrings.

"""
from abc import abstractmethod
from typing import List, Generator, Union

from ScrapyUtils.libs import Model
from . import Step


class Parse(Step):
    priority: int = 400

    @abstractmethod
    def parsing(self, content: str) -> Union[Generator[Model], List[Model]]:
        """The overriding method should pared the web page and should return the result.

        Args:
            content (str) : The content of the web page.

        Returns:
            List[Model]: The result of parsing.
        """
        pass
