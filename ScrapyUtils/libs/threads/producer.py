# -*- coding: utf-8 -*-
"""Consumer module.

生产者线程模块，提供了Producer类。

Producer样例：



Todo:
    * Multi producer will lock and block put

"""
from abc import abstractmethod
from collections import deque
from threading import Lock, Event
from typing import List, NoReturn, Any, Union

from queue import Queue, Full
from time import sleep

from .base_thread import BaseThread


class Producer(BaseThread):

    def __init__(self,
                 queue: Queue,
                 overflow: bool = True,
                 delay: Union[int, float] = 0.1,
                 lock: Lock = None,
                 event: Event = Event(), start_thread: bool = None, **kwargs):
        self.queue = queue
        self.delay = delay
        self.overflow = overflow
        self.lock = lock if lock else Lock()

        BaseThread.__init__(self, event, start_thread, **kwargs)

    @abstractmethod
    def producing(self):
        pass

    def run(self) -> None:
        while self.thread_wait():
            with self.lock:
                sleep(self.delay)

            self.current = None
            try:
                self.current = self.current if self.current else self.producing()
            except Exception as e:
                # TODO: log out
                self.pause(False)

            # TODO: lock and block put.
            if self.overflow:
                with self.lock:
                    while self.queue.full():
                        expire = self.queue.get()
                    self.queue.put(self.current)
            else:
                self.queue.put(self.current)

    def pause(self, block: bool = True):
        """Override pause of BaseThread. Producer cannot blocked pause.
        """
        super().pause(False)
