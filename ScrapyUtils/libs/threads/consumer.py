# -*- coding: utf-8 -*-
"""Consumer module.

消费者线程模块，提供了Consumer类。

Consumer样例：



Todo:
    * For module TODOs

"""
from abc import abstractmethod, ABCMeta
from typing import NoReturn, Any, Union
from logging import getLogger

from collections import deque
from queue import Queue
from threading import Lock, Event
from time import sleep

from .base_thread import BaseThread

logger = getLogger('consumer')


class BaseConsumer(BaseThread, metaclass=ABCMeta):
    """Base consumer. Extend it and override the consuming method to build custom consumer.

    只需要简单地继承并重写consuming方法，就可以快速创建各类的消费者线程类。
    """
    source: Union[Queue, deque]
    lock: Lock
    delay: Union[int, float]

    def __init__(self,
                 source: Any,
                 delay: Union[int, float] = 0.1,
                 lock: Lock = None,
                 event: Event = None,
                 start_thread: bool = True,
                 **kwargs):
        """除了BaseThread的参数，还需要source数据源、delay和lock作为同步延时锁。

        Args:
            source (Any): 消费者数据源
            delay (Union[int, float], optional): 每一次消费之间的间隔时间. Defaults to 0.1.
            lock (Lock, optional): 同步若干个消费者之间的间隔时间的锁. Defaults to None.
            event (Event, optional): 控制启停的event. Defaults to None.
            start_thread (bool, optional): 自动开启标志，True为自动开启. Defaults to True.
        """

        self.source = source
        self.delay = delay
        self.lock = lock if lock else Lock()

        BaseThread.__init__(self, event, start_thread, **kwargs)

    @abstractmethod
    def get_item(self) -> Any:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    def consuming_done(self):
        pass

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
                self.consuming_done()

    @abstractmethod
    def consuming(self, obj: Any) -> NoReturn:
        pass


class QueueConsumer(BaseConsumer):
    """基于队列的消费者"""
    source: Queue

    def get_item(self) -> Any:
        return self.source.get(timeout=0.01)

    def get_size(self) -> int:
        return self.source.qsize()

    def consuming_done(self):
        self.source.task_done()


class DequeConsumer(BaseConsumer):
    """基于双端队列的消费者"""
    source: deque

    def get_item(self) -> Any:
        return self.source.pop()

    def get_size(self) -> int:
        return len(self.source)
