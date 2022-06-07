# -*- coding: utf-8 -*-
"""Consumer module.

消费者线程模块，提供了Consumer类。

Consumer样例：



Todo:
    * For module TODOs

"""
from abc import abstractmethod
from typing import List, NoReturn, Any, Union, Dict, ClassVar, Tuple, Callable
from types import MethodType
from logging import getLogger

from collections import deque
from queue import Queue, Empty
from threading import Lock, Event
from time import sleep

from .base_thread import BaseThread

logger = getLogger('consumer')

support_source = [
    Queue,
    deque,
]


def _queue_get_item(self):
    source: Queue = self.source
    item = source.get(timeout=0.01)

    return item


def _queue_get_size(self):
    source: Queue = self.source
    return source.qsize()


def _deque_get_item(self):
    source: deque = self.source
    return source.popleft()


def _deque_get_size(self):
    source: deque = self.source
    return len(source)


class Consumer(BaseThread):
    """Base consumer. Extend it and override the consuming method to build custom consumer.

    只需要简单地继承并重写consuming方法，就可以快速创建各类的消费者线程类。
    """
    source: Union[Queue, deque]
    lock: Lock
    delay: Union[int, float]

    _get_item_mapper: Dict[type, Tuple[Callable, Callable]] = {
        Queue: (_queue_get_item, _queue_get_size),
        deque: (_deque_get_item, _queue_get_size),
    }

    def __init__(self,
                 source: Union[Queue, deque],
                 delay: Union[int, float] = 0.1,
                 lock: Lock = None,
                 event: Event = Event(),
                 start_thread: bool = True,
                 **kwargs):
        assert type(source) in support_source, 'Source not support'

        for cls, methods in self._get_item_mapper.items():
            if isinstance(source, cls):
                self.get_item = MethodType(methods[0], self)
                self.get_size = MethodType(methods[1], self)

        self.source = source

        self.delay = delay
        self.lock = lock if lock else Lock()

        BaseThread.__init__(self, event, start_thread, **kwargs)

    def get_item(self) -> Any:
        assert False

    def get_size(self) -> int:
        return 0

    def run(self) -> NoReturn:
        while self.thread_wait():

            with self.lock:
                sleep(self.delay)

            # step 1: get obj.
            try:
                obj = self.get_item()
            except Exception as e:
                # print(e.__class__, e)
                continue

            # step 2: consume obj.
            try:
                self.consuming(obj)
            except Exception as e:
                logger.exception(exc_info=e, msg='consuming error')
                self.pause(False)
            else:
                # TODO:
                if issubclass(self.source.__class__, Queue):
                    self.source.task_done()

    @abstractmethod
    def consuming(self, obj: Any) -> NoReturn:
        pass


if __name__ == '__main__':
    number = 0


    class Count(Consumer):
        def consuming(self, obj: Any) -> NoReturn:
            global number
            number += 0
            print(obj)


    queue = Queue()

    [queue.put(x) for x in range(100)]

    count = Count(source=queue)
