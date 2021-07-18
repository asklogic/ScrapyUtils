# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Todo:
    * For module TODOs
    
"""

from abc import abstractmethod
from typing import Optional, Any, NoReturn
from collections import deque

from .base_thread import BasicThread


class DequeThread(BasicThread):

    @property
    def deque(self) -> deque:
        return self._source


class Consumer(DequeThread):

    @abstractmethod
    def consuming(self) -> Any:
        pass

    def do_loop(self):
        item = self.consuming()
        self.deque.append(item)


class Producer(DequeThread):
    @abstractmethod
    def producing(self, item: Any) -> NoReturn:
        pass

    def do_loop(self):
        item = self.deque.popleft()

        self.producing(item)
