# -*- coding: utf-8 -*-
"""Consumer module.

消费者线程模块，提供了Consumer类。

Consumer样例：



Todo:
    * For module TODOs

"""
from abc import abstractmethod
from threading import Lock, Event
from typing import List, NoReturn, Any, Union

from queue import Queue, Empty, Full
from time import sleep

from .base_thread import BaseThread


class Consumer(BaseThread):
    """Base consumer. Extend it and override the consuming method to build custom consumer.

    只需要继承并重写consuming方法，就可以快速创建各类简单的消费者模型。
    """
    queue: Queue
    lock: Lock
    delay: Union[int, float]

    def __init__(self,
                 queue: Queue,
                 delay: Union[int, float] = 0.1,
                 lock: Lock = None,
                 event: Event = Event(), start_thread: bool = None, **kwargs):

        self.queue = queue
        self.delay = delay
        self.lock = lock if lock else Lock()

        # BaseThread.__init__(self, **kwargs)

        BaseThread.__init__(self, event, start_thread, **kwargs)

    def run(self) -> NoReturn:
        while self.thread_wait():

            with self.lock:
                sleep(self.delay)

            # step 1: get obj.
            try:
                obj = self.queue.get(timeout=0.05)
            except Empty as e:
                continue
            else:
                self.queue.task_done()

            # step 2: consume obj.
            try:
                self.consuming(obj)
            except Exception as e:
                self.pause(False)

    def wait_exit(self) -> NoReturn:
        while self.queue.qsize() != 0:
            sleep(0.01)

    @abstractmethod
    def consuming(self, obj: Any) -> NoReturn:
        pass
