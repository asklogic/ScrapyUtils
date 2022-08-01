# -*- coding: utf-8 -*-
"""Producer module.

生产者线程模块，提供了Producer类。

Producer样例：



Todo:
    * Multi producer will lock and block put

"""
from abc import abstractmethod, ABCMeta
from collections import deque
from collections.abc import Iterator
from logging import getLogger
from threading import Lock, Event
from typing import Any, Union, NoReturn

from queue import Queue
from time import sleep

from ScrapyUtils.libs.threads.base_thread import BaseThread

logger = getLogger('producing')


class BaseProducer(BaseThread, metaclass=ABCMeta):
    """基础的生产者"""
    source: Union[Queue, deque]
    lock: Lock
    delay: Union[int, float]

    current = None
    """当前Producing的对象"""

    def __init__(self,
                 source: Any,
                 delay: Union[int, float] = 0.1,
                 lock: Lock = None,
                 event: Event = None,
                 start_thread: bool = True,
                 **kwargs):
        """除了BaseThread的参数，还需要source数据源、delay和lock作为同步延时锁。

        Args:
            source (Any): 生产者数据源
            delay (Union[int, float], optional): 每一次生产之间的间隔时间. Defaults to 0.1.
            lock (Lock, optional): 同步若干个生产者之间的间隔时间的锁. Defaults to None.
            event (Event, optional): 控制启停的event. Defaults to None.
            start_thread (bool, optional): 自动开启标志，True为自动开启. Defaults to True.
        """

        self.source = source
        self.delay = delay
        self.lock = lock if lock else Lock()

        BaseThread.__init__(self, event, start_thread, **kwargs)

    @abstractmethod
    def producing(self) -> Any:
        pass

    @abstractmethod
    def put_item(self, item) -> NoReturn:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    def run(self) -> None:
        while self.thread_wait():
            with self.lock:
                sleep(self.delay)

            try:
                item = self.producing()
                if isinstance(item, Iterator):
                    [self.put_item(_) for _ in item]
                else:
                    self.put_item(item)

                self.current = self.current if self.current is not None else self.producing()
            except Exception as e:
                logger.exception(exc_info=e, msg='consuming error')
                self.pause(False)

    def pause(self, block: bool = True):
        # TODO: but why?
        """Override pause of BaseThread. Producer cannot block pause.
        """
        super().pause(False)


class DequeProducer(BaseProducer):
    """基于双端队列的生产者"""
    source: deque

    def put_item(self, item) -> NoReturn:
        self.source.append(item)

    def get_size(self) -> int:
        return len(self.source)


class QueueProducer(BaseProducer):
    """基于队列的生产者"""
    source: Queue

    def put_item(self, item) -> NoReturn:
        self.source.put(item)

    def get_size(self) -> int:
        return self.source.qsize()
