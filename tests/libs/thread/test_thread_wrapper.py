import unittest
import time
from multiprocessing import Pool as ThreadPool
from concurrent.futures import TimeoutError, ThreadPoolExecutor
from threading import Thread

from base.libs import ThreadWrapper
from typing import Callable


class _ThreadWrapper(Thread):

    def __init__(self, callable: Callable, args=None, kwargs=None, timeout=3):
        # thread property
        super(_ThreadWrapper, self).__init__()
        self.setDaemon(True)

        self.callable = callable
        self.timeout = timeout
        self.args = args
        self.kwargs = kwargs

        # property
        self._result = None

    # def run(self) -> None:
    #     current_pool = ThreadPoolExecutor(1)
    #     future = current_pool.submit(self.callable, *self.args)
    #     try:
    #         self._result = future.result(self.timeout)
    #     except TimeoutError as te:
    #         pass
    #     current_pool.shutdown(False)
    #     # TODO:sys garbage collect?

    def run(self) -> None:
        t = Thread(target=self.callable, args=self.args,kwargs=self.kwargs)
        t.setDaemon(True)
        t.start()
        time.sleep(self.timeout)
        print('inner join done.')


    @property
    def result(self):
        return self._result


def inner(timeout):
    time.sleep(timeout)
    print('#done#')


class ThreadWrapperTestCase(unittest.TestCase):
    def test_something(self):
        t = _ThreadWrapper(inner, args=(2,), timeout=1)
        t.start()
        t.join()


        time.sleep(4)

    def test_demo(self):
        t = ThreadWrapper(inner, args=(2,), timeout=1)
        t.start()
        t.join()
        print('join done')
        del t

        time.sleep(3)

    def test_critical(self):
        pass


if __name__ == '__main__':
    unittest.main()
