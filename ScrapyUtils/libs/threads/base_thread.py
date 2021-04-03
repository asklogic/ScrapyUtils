# -*- coding: utf-8 -*-
"""BaseThread module.

基础线程模块，提供了BaseThread常用线程类。

BaseThread样例：



Todo:
    * nothing.

.. python threading library:
    cn: https://docs.python.org/zh-cn/3/library/threading.html

"""
from abc import abstractmethod
from typing import List, NoReturn

from collections import deque
from multiprocessing.dummy import Pool as ThreadPool
from queue import Queue, Empty, Full
from time import sleep
from threading import Event, Thread, Condition, Barrier


class BaseThread(Thread):
    """BaseThread for Consumer/Producer base on Threading.Thread.

    通过操作Condition来提供简单的启停操作。

    Args:
        Thread (threading.Thread): 线程基类
    """

    condition: Condition

    def __init__(self, **kwargs):
        """Override the Thread.__init__.

        默认设置为守护进程，也可以添加Thread的参数。

        初始化condition操作，默认阻塞。

        Args:
            condition (condition, optional): threading.condition to control start/stop. Defaults to None.
        """
        if condition:
            assert isinstance(condition, Condition), 'Need condition instance.'

        daemon = dict(kwargs).pop('daemon', True)
        Thread.__init__(self, daemon=daemon, **kwargs)

        # self.condition.acquire()

    @abstractmethod
    def run(self) -> None:
        """A sample run function.

        The condition will be blocked in main run if condition is locked.

        不断执行一个需要一定时间执行的方法。每次运行时，控制condition来进行启停操作。
        """
        while self.condition.wait():
            sleep(1)
            print('run')


class Mock(BaseThread):

    def __init__(self, event=None, **kwargs):
        self.count = 0
        # self.flag = True
        self.event = event if event else Event()
        self.event.set()

        # self.event.clear()

        self.condition = Condition()
        with self.condition:
            self.paused = True

        self.barrier = Barrier(2)
        super().__init__(**kwargs)

    def run(self) -> None:
        while True:
            # with self.condition:
            # print('inner')
            # self.condition.acquire()

            if self.paused:
                print('inner wait before', self.barrier.n_waiting)
                if self.barrier.n_waiting == 1:
                    self.barrier.wait()
                self.barrier.wait()
                print('inner wait after', self.barrier.n_waiting)


            self.event.wait()

            print('single task start')

            # self.event.wait
            for i in range(5):
                print('do task', i + 1, self.name)

                sleep(1)
                self.count += 1

            # self.condition.release()

            # print('task done.', self.count, self.name)

    def pause(self, block: bool = True):
        # with self.condition:
        # self.condition.acquire(block)
        if not self.paused:
            self.paused = True

            if block:
                self.barrier.wait()
        # self.condition.release()
        # self.barrier.wait()

    def resume(self, block=False):
        # with self.condition:
        if self.paused:
            self.paused = False
            self.barrier.wait()

        # self.condition.acquire(block)
        # self.flag = False
        # self.condition.notify_all()
        # self.condition.release()

    def f(self):
        with self.condition:
            # raise RuntimeError()
            self.paused = False
            self.condition.notify_all()


if __name__ == '__main__':
    condition = Condition()
    mock0 = Mock()
    mock1 = Mock()
    mock0.start()
    mock1.start()
    pass
