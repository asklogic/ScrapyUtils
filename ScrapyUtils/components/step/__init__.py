# -*- coding: utf-8 -*-
"""Step module for http action.

Todo:
    * For module TODOs
    
"""

from abc import abstractmethod
from ScrapyUtils.components import Component

from .suit import StepSuit


class Step(Component):
    """
    Step is base class for Action and Parse.

    Step类是Action和Parse的基类，所有的爬取操作和解析操作都会封装为一个个不同的Step类。其中Action类负责如http访问等获取数据的操作，而Parse负责处理数据。

    所有的Step类在同一个线程中，都拥有同一个Suit实例来管理。这一系列Step实例的context属性也指向其Suit实例的context属性，用于同一线程下的上下文管理。
    """

    suit: StepSuit = None

    @property
    def context(self) -> dict:
        """
        The shared property from a step's suit.

        返回suit对象的context字典属性以实现共享context。

        Returns:
            dict: The suit's context property.
        """
        return self.suit.context
