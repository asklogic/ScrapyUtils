# -*- coding: utf-8 -*-
"""Producer module.

生产者线程模块，提供了Producer类。

Producer样例：



Todo:
    * Multi producer will lock and block put

"""
from abc import abstractmethod
from collections import deque
from threading import Lock, Event
from typing import Any, Dict, List, Tuple, Union, Callable
from types import MethodType

from queue import Queue, Full
from time import sleep

from ScrapyUtils.libs.threads import BaseThread


def _queue_put_item(self, item):
    source: Queue = self.source
    source.put(item, timeout=0.01)


def _queue_get_size(self):
    source: Queue = self.source
    return source.qsize()


def _deque_put_item(self, item):
    source: deque = self.source
    return source.append(item)


def _deque_get_size(self):
    source: deque = self.source
    return len(source)


class Producer(BaseThread):
    source: Union[Queue, deque]
    lock: Lock
    delay: Union[int, float]

    _get_item_mapper: Dict[type, Tuple[Callable, Callable]] = {
        Queue: (_queue_put_item, _queue_get_size),
        deque: (_deque_put_item, _queue_get_size),
    }

    def __init__(self,
                 source: Union[Queue, deque],
                 delay: Union[int, float] = 0.1,
                 lock: Lock = None,
                 expire: bool = True,
                 event: Event = Event(), start_thread: bool = None, **kwargs):

        for cls, methods in self._get_item_mapper.items():
            if isinstance(source, cls):
                self.put_item = MethodType(methods[0], self)
                self.get_size = MethodType(methods[1], self)

        self.source = source

        self.delay = delay
        self.lock = lock if lock else Lock()
        self.expire = expire

        BaseThread.__init__(self, event, start_thread, **kwargs)

    @abstractmethod
    def producing(self):
        pass

    def put_item(self, item):
        pass

    def get_size(self) -> int:
        pass

    def run(self) -> None:
        while self.thread_wait():
            with self.lock:
                sleep(self.delay)

            if self.expire:
                self.current = None
            try:
                self.current = self.current if self.current else self.producing()
            except Exception as e:
                # TODO: log out
                print(e)
                self.pause(False)
            else:
                self.put_item(self.current)

    def pause(self, block: bool = True):
        """Override pause of BaseThread. Producer cannot blocked pause.
        """
        super().pause(False)


if __name__ == '__main__':
    number = 0


    class Count(Producer):

        def producing(self):
            global number
            number += 1
            return number


    queue = Queue()

    count = Count(source=queue)
