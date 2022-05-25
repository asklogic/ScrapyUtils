# -*- coding: utf-8 -*-
"""BaseThread module.

基础线程模块，提供了BaseThread常用线程类。

BaseThread样例：

Todo:
    * nothing.

.. python threading library:
    en: https://docs.python.org/3/library/threading.html
    cn: https://docs.python.org/zh-cn/3/library/threading.html

"""
import threading
import time
from abc import abstractmethod

from time import sleep
from threading import Event, Thread, Condition, Barrier

# global setting:
from typing import Optional, Callable, Any, Iterable, Mapping

initial_start_thread = False


class BaseThread(Thread):
    """BaseThread for Consumer/Producer base on Threading.Thread.

    通过操作Barrier来提供简单的启停操作。
    """
    _paused_flag = True

    barrier: Barrier
    event: Event

    def __init__(self, event: Event = Event(), start_thread: bool = True, **kwargs):
        """Override the Thread.__init__.

        默认设置为守护进程，也可以添加Thread的参数。
        """

        # Default barrier.
        # The parties is 2 thread : main thread and sub thread.
        self.barrier = Barrier(2)

        # The optional arguments: shared event.
        self.event = event
        self.event.set()

        # Default daemon.
        daemon = dict(kwargs).pop('daemon', True)
        Thread.__init__(self, daemon=daemon, **kwargs)
        # Thread.__init__(self, **kwargs)

        # The optional arguments: start_thread
        # start_thread = dict(kwargs).pop('start_thread', initial_start_thread)

        flag = start_thread if start_thread is not None else initial_start_thread
        if flag:
            Thread.start(self)

    @property
    def stopped(self) -> bool:
        """The state of BaseThread.
        """
        if self.paused_flag and self.barrier.n_waiting == 1:
            return True
        else:
            return False

    @property
    def paused_flag(self) -> bool:
        """The pause state of BaseThread.
        """

        return self._paused_flag

    @paused_flag.setter
    def paused_flag(self, value):
        """
        Setter of property paused_flag

        If ture mean pause thread, invoke on_pause()
        If false mean resume thread, invoke on_resume()

        Args:
            value (bool): The value of paused_flag.
        """
        if value:
            self.on_pause()
            self._paused_flag = True
        else:
            self._paused_flag = False
            self.on_resume()

    @abstractmethod
    def run(self) -> None:
        """A sample run function.

        不断执行一个需要一定时间执行的方法。每次运行时，控制barrier来进行启停操作。
        """
        while self.thread_wait():
            sleep(1)
            print('run', self.name)

    def thread_wait(self):
        """
        The BaseThread wait in a loop.

        Returns:
            bool: Always True.
        """
        if self.paused_flag:
            self.barrier_wait()
        self.event.wait()

        return True

    def barrier_wait(self):
        """The BaseThread sync-wait in thread_wait().

        通过控制两个长度的barrier来控制子线程的启停。

        每次线程暂停时，子线程通过parsed_flag来判断是否需要暂停：
            如果不需要，则正常运行。
            如果需要暂停，则调用barrier.wait()暂停。
                如果父线程是非阻塞式暂停，只需要修改parsed_flag即可暂停线程。
                如果父线程是阻塞是暂停：
                    1.父线程也会调用wait，阻塞等待子线程暂停。
                    2.当子线程也运行至wait()，会判断是否父线程是否已经阻塞，如果阻塞，子线程则会添加一次wait()操作。
                    这样父线程不再阻塞，而子线程继续阻塞暂停。

        # TODO: refactor to shared barrier between BaseThread.
        """
        if self.paused_flag:
            # If main thread wait because pause, release it ...
            if self.barrier.n_waiting == self.barrier.parties - 1:
                self.barrier.wait()
            # and wait in sub thread.
            self.barrier.wait()
        return True

    # common method:
    def pause(self, block: bool = True):
        """
        Pause a BaseThread in thread_wait.

        If block, the main thread will block until the sub thread wait.
        If not block, just set the paused_flag to True.

        Args:
            block (bool, optional): Block pause or not. Defaults to True.
        """
        if not self.paused_flag:
            self.paused_flag = True

            if block:
                self.barrier.wait()

    def resume(self):
        """
        Resume a BaseThread from thread_wait.

        Set the paused_flag to fasle and check the n_waiting.

        If the sub thread is waiting, the main thread will wait.
        """
        if self.paused_flag:
            self.paused_flag = False
            if self.barrier.n_waiting != 0:
                self.barrier.wait()

    @abstractmethod
    def on_pause(self):
        pass

    @abstractmethod
    def on_resume(self):
        pass


class BasicThread(threading.Thread):
    """最简单的基础线程类
    
    只提供基本的启动和循环方法，以及终止循环和异常处理的方法。

    要使用需要重写do_loop函数。
    """

    def __init__(self, source, delay: int = 1, daemon: Optional[bool] = ...) -> None:
        """屏蔽了大多数Thread类的init参数"""

        self._source = source
        self.delay = delay
        super().__init__(daemon=daemon)

    @abstractmethod
    def on_start(self):
        """on_start 线程类开始时执行的方法。
        """
        pass

    def start(self) -> None:
        self.on_start()
        super().start()

    @abstractmethod
    def do_loop(self):
        pass

    @abstractmethod
    def break_condition(self) -> bool:
        """break_condition 退出循环的条件，返回为True则退出循环进而退出线程。每次循环前都会执行此方法。

        Returns:
            bool: 是否退出循环的标志，如果返回值布尔运算为True则退出。
        """
        pass

    @abstractmethod
    def exception_callback(self, exception: Exception):
        """exception_callback 处理异常的方法，当do_loop出现异常时执行此方法。

        Args:
            exception (Exception): do_loop抛出的异常。
        """
        pass

    def run(self) -> None:
        while True:
            # 先检查是否退出循环
            if self.break_condition():
                break
            # 执行do_loop方法
            try:
                self.do_loop()
            # 如果捕获异常
            except Exception as e:
                # 执行相关方法
                self.exception_callback(e)
            finally:
                time.sleep(max(0, self.delay))
