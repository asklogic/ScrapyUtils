# -*- coding: utf-8 -*-
"""Example Google style docstrings.

"""
from abc import abstractmethod
from typing import Iterable, Union, Sequence, Optional

from ScrapyUtils.libs import Model
from . import Step


class Parse(Step):
    priority: int = 400

    @abstractmethod
    def parsing(self, content: str) -> Optional[Union[Iterable[Model], Sequence[Model]]]:
        """The overriding method should pared the web page and should return the result.

        Args:
            content (str) : The content of the web page.

        Returns:
            Union[Iterable[Model], List[Model]]: The parsed result.
        """
        pass
