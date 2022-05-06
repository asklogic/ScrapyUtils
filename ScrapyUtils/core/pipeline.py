# -*- coding: utf-8 -*-
"""Pipeline Module to process models base on ProcessorSuit.

Todo:
    * For module TODOs
    
"""
from collections import deque
from logging import getLogger
from queue import Queue
from threading import Lock, Event
from typing import Any, NoReturn, Union

from ScrapyUtils.components import ProcessorSuit

from ScrapyUtils.libs import Consumer, Model

logger = getLogger(__name__)


class Pipeline(Consumer):
    suit: ProcessorSuit = None

    failed: deque
    remain: deque

    def __init__(self,
                 source: Union[Queue, deque],
                 suit: ProcessorSuit,
                 delay: Union[int, float] = 0, lock: Lock = None,
                 event: Event = Event(), start_thread: bool = None, **kwargs):
        assert isinstance(suit, ProcessorSuit), 'Pipeline need a suit instance.'

        self.suit: ProcessorSuit = suit  # ProcessorSuit: The processor suit to process model.
        self.failed: deque = deque()  # deque: The models failed in process.
        self.remain: deque = deque()  # deque: The remained models when pipeline exit.

        super().__init__(source, delay, lock, event, start_thread, **kwargs)

    def consuming(self, obj: Model) -> NoReturn:
        """Process every model by suit.process method."""
        try:
            self.suit.process(model=obj)
        except Exception as e:
            logger.error('Process model failed.', exc_info=e)
            self.failed.append(obj)
        else:
            pass

    def exit(self):
        """Paused, dump to remain and exit."""
        self.pause(True)

        if self.get_size() > 0:
            model = self.get_item()
            self.remain.append(model)
