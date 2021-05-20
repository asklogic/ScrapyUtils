# -*- coding: utf-8 -*-
"""Components scheme.

构建StepSuit列表和ProcessorSuit，实例化各项组件类。

Todo:
    * Refactor components on_start/on_exit.

"""

from .scheme import Scheme

from ScrapyUtils import configure
from ScrapyUtils.components import StepSuit, ProcessorSuit


class ComponentsScheme(Scheme):

    @classmethod
    def start(cls):
        steps_class = configure.steps_class
        processors_class = configure.processors_class

        thread = configure.THREAD

        step_suits = [StepSuit(components=steps_class) for i in range(thread)]
        processor_suit = ProcessorSuit(processors_class)

        configure.step_suits = step_suits
        configure.processor_suit = processor_suit

    @classmethod
    def verify(self) -> bool:
        assert configure.step_suits
        assert configure.processor_suit
        return True

    @classmethod
    def stop(self):
        for suit in configure.step_suits:
            suit.suit_exit()

        configure.processor_suit.suit_exit()