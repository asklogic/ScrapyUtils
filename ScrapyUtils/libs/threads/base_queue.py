# -*- coding: utf-8 -*-
"""基于Python原生队列的消费者、生产者类。

兼容各种与原生队列相同的数据源
"""
from abc import abstractmethod
from typing import Any, NoReturn
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
