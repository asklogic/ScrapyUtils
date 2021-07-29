# -*- coding: utf-8 -*-
"""steps package.

负载执行各类操作的包。

将人在浏览器上的各种操作抽象为Step类，通过执行一系列独立的Step来完成一次正常的访问流程。

Step跟据其性质拆分为两大类：

    1. Action: 包括HTTP在内的访问操作，此类操作会从其他服务器中获取数据。
    2. Parse: 从文字里面获取信息的解析操作，此类操作仅仅是从页面的数据中解析得到格式化数据。

Step继承自Component，通过StepSuit来统一启停，并且通过StepSuit的方法来完成一次流程。

Package结构:
    1. __init__: Step类
    2. action: Action类模块
    3. parse: Parse类模块
    4. suit: StepSuit模块

"""
from abc import abstractmethod
from ScrapyUtils.components import Component


class Step(Component):
    """
    Step is base class for Action and Parse.

    Step类是Action和Parse的基类，所有的爬取操作和解析操作都会封装为一个个不同的Step类。

    其中Action类负责如http访问等获取数据的操作，而Parse负责处理数据。
    """
    _context: dict = None

    @property
    def context(self) -> dict:
        """
        The shared property from a step's suit.

        StepSuit会放入同一个dict，以此实现一组Step共用同一个context。

        Returns:
            dict: The suit's context property.
        """
        return self._context


# relative
from .action import Action
from .parse import Parse
from .suit import StepSuit
