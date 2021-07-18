# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Todo:
    * For module TODOs
    
"""
from abc import abstractmethod
from typing import Optional, Any, NoReturn
from queue import Queue

from .base_thread import BasicThread


class QueueThread(BasicThread):

    @property
    def queue(self) -> Queue:
        return self._source


class Consumer(QueueThread):

    @abstractmethod
    def consuming(self) -> Any:
        pass

    def do_loop(self):
        item = self.consuming()
        self.queue.put(item)


class Producer(QueueThread):
    @abstractmethod
    def producing(self, item: Any) -> NoReturn:
        pass

    def do_loop(self):
        item = self.queue.get(block=True)

        self.producing(item)

        self.queue.task_done()
